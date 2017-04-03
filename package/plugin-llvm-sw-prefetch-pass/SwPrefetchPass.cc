#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Module.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/InstVisitor.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/ValueMap.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/ADT/SetVector.h"
#include "llvm/IR/Verifier.h"
#include "llvm/Analysis/ValueTracking.h"
#include "llvm/Transforms/Scalar.h"

#include "llvm/Support/raw_ostream.h"

#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>


#include <iostream>
#include <map>

#include <llvm/Support/Debug.h>

#ifdef NO_STRIDES
#define C_CONSTANT (32)
#else 
#define C_CONSTANT (64)
#endif

using namespace llvm;


namespace {

struct SwPrefetchPass : FunctionPass, InstVisitor<SwPrefetchPass>
{
    /// The module that we're currently working on
    Module *M = 0;
    /// The data layout of the current module.
    DataLayout *DL = 0;
    /// Unique value.  Its address is used to identify this class.
    static char ID;
    /// Call the superclass constructor with the unique identifier as the
    /// (by-reference) argument.

    SwPrefetchPass() : FunctionPass(ID) {}


    /// Return the name of the pass, for debugging.
    const char *getPassName() const override {
        return "Indirect Software Prefetch";
    }



    /// doInitialization - called when the pass manager begins running this
    /// pass on a module.  A single instance of the pass may be run on multiple
    /// modules in sequence.
    bool doInitialization(Module &Mod) override {
        M = &Mod;
        if (DL)
            delete DL;
        DL = new DataLayout(M);
        // Return false on success.

        return false;
    }

    /// doFinalization - called when the pass manager has finished running this
    /// pass on a module.  It is possible that the pass will be used again on
    /// another module, so reset it to its initial state.
    bool doFinalization(Module &Mod) override {
        assert(&Mod == M);




        delete DL;
        M = nullptr;
        DL = nullptr;
        // Return false on success.

        return false;
    }



    virtual void getAnalysisUsage(AnalysisUsage& AU) const override {
        AU.addRequired<LoopInfoWrapperPass>();
    }


    bool makeLoopInvariantSpec(Instruction *I, bool &Changed, Loop* L) const {
        // Test if the value is already loop-invariant.
        if (L->isLoopInvariant(I))
            return true;
        // EH block instructions are immobile.
        // Determine the insertion point, unless one was given.
        if(!I) return false;
        if(!isSafeToSpeculativelyExecute(I) && !I->mayReadFromMemory()) return false; //hacky af but it works for now.

        BasicBlock *Preheader = L->getLoopPreheader();
        // Without a preheader, hoisting is not feasible.
        if (!Preheader)
            return false;
        Instruction* InsertPt = Preheader->getTerminator();

        // Don't hoist instructions with loop-variant operands.
        for (Value *Operand : I->operands())
            if(Instruction* i = dyn_cast<Instruction>(Operand)) if (!makeLoopInvariantSpec(i, Changed, L)) {
                    Changed = false;
                    return false;
                }

        // Hoist.
        I->moveBefore(InsertPt);

        // There is possibility of hoisting this instruction above some arbitrary
        // condition. Any metadata defined on it can be control dependent on this
        // condition. Conservatively strip it here so that we don't give any wrong
        // information to the optimizer.

        Changed = true;
        return true;
    }

    Value *getCanonicalishSizeVariable(Loop* L) const {

        // Loop over all of the PHI nodes, looking for a canonical indvar.


        auto B = L->getExitingBlock();

        if(!B) return nullptr;




        for(Instruction &J : *B) {

            Instruction* I = &J;
            CmpInst *CI = dyn_cast<CmpInst>(I);


            bool Changed = false;

            if(CI) {
                if(L->makeLoopInvariant(CI->getOperand(1),Changed)) return CI->getOperand(1);

                if(L->makeLoopInvariant(CI->getOperand(0),Changed)) return CI->getOperand(0);

                dbgs() << "Size not loop invariant!" << *(CI->getOperand(0)) << *(CI->getOperand(1)) << "\n";
            }



        }



        return nullptr;
    }

    PHINode *getCanonicalishInductionVariable(Loop* L) const {
        BasicBlock *H = L->getHeader();

        BasicBlock *Incoming = nullptr, *Backedge = nullptr;
        pred_iterator PI = pred_begin(H);
        assert(PI != pred_end(H) &&
               "Loop must have at least one backedge!");
        Backedge = *PI++;
        if (PI == pred_end(H)) return nullptr;  // dead loop
        Incoming = *PI++;
        if (PI != pred_end(H)) return nullptr;  // multiple backedges?

        if (L->contains(Incoming)) {
            if (L->contains(Backedge))
                return nullptr;
            std::swap(Incoming, Backedge);
        } else if (!L->contains(Backedge))
            return nullptr;


        // Loop over all of the PHI nodes, looking for a canonical indvar.
        for (BasicBlock::iterator I = H->begin(); isa<PHINode>(I); ++I) {
            PHINode *PN = cast<PHINode>(I);
            if (Instruction *Inc =
                        dyn_cast<Instruction>(PN->getIncomingValueForBlock(Backedge)))
                if (Inc->getOpcode() == Instruction::Add &&
                        Inc->getOperand(0) == PN)
                    if (dyn_cast<ConstantInt>(Inc->getOperand(1)))
                        return PN;
        }
        return nullptr;
    }


    PHINode *getWeirdCanonicalishInductionVariable(Loop* L) const {
        BasicBlock *H = L->getHeader();

        BasicBlock *Incoming = nullptr, *Backedge = nullptr;
        pred_iterator PI = pred_begin(H);
        assert(PI != pred_end(H) &&
               "Loop must have at least one backedge!");
        Backedge = *PI++;
        if (PI == pred_end(H)) return nullptr;  // dead loop
        Incoming = *PI++;
        if (PI != pred_end(H)) return nullptr;  // multiple backedges?

        if (L->contains(Incoming)) {
            if (L->contains(Backedge))
                return nullptr;
            std::swap(Incoming, Backedge);
        } else if (!L->contains(Backedge))
            return nullptr;

        // Loop over all of the PHI nodes, looking for a canonical indvar.
        for (BasicBlock::iterator I = H->begin(); isa<PHINode>(I); ++I) {
            PHINode *PN = cast<PHINode>(I);
            if (GetElementPtrInst *Inc =
                        dyn_cast<GetElementPtrInst>(PN->getIncomingValueForBlock(Backedge)))
                if (Inc->getOperand(0) == PN)
                    if (ConstantInt *CI = dyn_cast<ConstantInt>(Inc->getOperand(Inc->getNumOperands()-1)))
                        if (CI->equalsInt(1))
                            return PN;
        }
        return nullptr;
    }


    GetElementPtrInst *getWeirdCanonicalishInductionVariableGep(Loop* L) const {
        BasicBlock *H = L->getHeader();

        BasicBlock *Incoming = nullptr, *Backedge = nullptr;
        pred_iterator PI = pred_begin(H);
        assert(PI != pred_end(H) &&
               "Loop must have at least one backedge!");
        Backedge = *PI++;
        if (PI == pred_end(H)) return nullptr;  // dead loop
        Incoming = *PI++;
        if (PI != pred_end(H)) return nullptr;  // multiple backedges?

        if (L->contains(Incoming)) {
            if (L->contains(Backedge))
                return nullptr;
            std::swap(Incoming, Backedge);
        } else if (!L->contains(Backedge))
            return nullptr;

        // Loop over all of the PHI nodes, looking for a canonical indvar.
        for (BasicBlock::iterator I = H->begin(); isa<PHINode>(I); ++I) {
            PHINode *PN = cast<PHINode>(I);
            if (GetElementPtrInst *Inc =
                        dyn_cast<GetElementPtrInst>(PN->getIncomingValueForBlock(Backedge)))
                if (Inc->getOperand(0) == PN)
                    if (ConstantInt *CI = dyn_cast<ConstantInt>(Inc->getOperand(Inc->getNumOperands()-1)))
                        if (CI->equalsInt(1))
                            return Inc;
        }
        return nullptr;
    }


    Value *getWeirdCanonicalishInductionVariableFirst(Loop* L) const {
        BasicBlock *H = L->getHeader();

        BasicBlock *Incoming = nullptr, *Backedge = nullptr;
        pred_iterator PI = pred_begin(H);
        assert(PI != pred_end(H) &&
               "Loop must have at least one backedge!");
        Backedge = *PI++;
        if (PI == pred_end(H)) return nullptr;  // dead loop
        Incoming = *PI++;
        if (PI != pred_end(H)) return nullptr;  // multiple backedges?

        if (L->contains(Incoming)) {
            if (L->contains(Backedge))
                return nullptr;
            std::swap(Incoming, Backedge);
        } else if (!L->contains(Backedge))
            return nullptr;

        // Loop over all of the PHI nodes, looking for a canonical indvar.
        for (BasicBlock::iterator I = H->begin(); isa<PHINode>(I); ++I) {
            PHINode *PN = cast<PHINode>(I);
            if (GetElementPtrInst *Inc =
                        dyn_cast<GetElementPtrInst>(PN->getIncomingValueForBlock(Backedge)))
                if (Inc->getOperand(0) == PN)
                    if (ConstantInt *CI = dyn_cast<ConstantInt>(Inc->getOperand(Inc->getNumOperands()-1)))
                        if (CI->equalsInt(1))
                            return PN->getIncomingValueForBlock(Incoming);
        }
        return nullptr;
    }

    Value *getOddPhiFirst(Loop* L, PHINode* PN) const {
        BasicBlock *H = L->getHeader();

        BasicBlock *Incoming = nullptr, *Backedge = nullptr;
        pred_iterator PI = pred_begin(H);
        assert(PI != pred_end(H) &&
               "Loop must have at least one backedge!");
        Backedge = *PI++;
        if (PI == pred_end(H)) return nullptr;  // dead loop
        Incoming = *PI++;
        if (PI != pred_end(H)) return nullptr;  // multiple backedges?

        if(H != PN->getParent()) return nullptr;

        if (L->contains(Incoming)) {
            if (L->contains(Backedge))
                return nullptr;
            std::swap(Incoming, Backedge);
        } else if (!L->contains(Backedge))
            return nullptr;

        return PN->getIncomingValueForBlock(Incoming);

    }




    bool depthFirstSearch (Instruction* I, LoopInfo &LI, Instruction* &Phi, SmallVector<Instruction*,8> &Instrs, SmallVector<Instruction*,4> &Loads, SmallVector<Instruction*,4> &Phis, std::vector<SmallVector<Instruction*,8>>& Insts) {
        Use* u = I->getOperandList();
        Use* end = u + I->getNumOperands();

        SetVector<Instruction*> roundInsts;

        bool found = false;

        for(Use* v = u; v<end; v++) {

            PHINode* p = dyn_cast<PHINode>(v->get());
            Loop* L = nullptr;
            if(p) L = LI.getLoopFor(p->getParent());

            if(p && L && (p == getCanonicalishInductionVariable (L) || p == getWeirdCanonicalishInductionVariable(L))) {



                dbgs() << "Loop induction phi node! " << *p << "\n";

                if(Phi) {
                    if(Phi == p) {
                        //add this
                        roundInsts.insert (p);
                        found = true; //should have been before anyway
                    } else {
                        //check which is older.
                        if(LI.getLoopFor(Phi->getParent())->isLoopInvariant(p)) {
                            //do nothing
                            dbgs() << "not switching phis\n";
                        } else if (LI.getLoopFor(p->getParent())->isLoopInvariant(Phi)) {
                            dbgs() << "switching phis\n";
                            roundInsts.clear();
                            roundInsts.insert (p);
                            Phi = p;
                            found = true;
                        } else {
                            assert(0);
                        }
                    }
                } else {

                    Phi = p;
                    roundInsts.insert (p);
                    found = true;
                }



            }
            else if(dyn_cast<StoreInst>(v->get())) {}
            else if(dyn_cast<CallInst>(v->get())) {}
            else if(dyn_cast<TerminatorInst>(v->get())) {}
            else if(LoadInst * linst = dyn_cast<LoadInst>(v->get())) {
				//Cache results
        
        int lindex=-1;
        int index=0;
			for( auto l: Loads) {
				if (l == linst) {lindex=index; break;}
				index++;
			} 
			
			if(lindex!=-1) {
				Instruction* phi = Phis[lindex];
				
				if(Phi) {
                    if(Phi == phi) {
                                //add this
                                for(auto q : Insts[lindex]) roundInsts.insert (q);
                                found = true; //should have been before anyway
                    } else {
                                //check which is older.
                                if(LI.getLoopFor(Phi->getParent())->isLoopInvariant(phi)) {
                                    //do nothing
                                    dbgs() << "not switching phis\n";
                                } else if (LI.getLoopFor(phi->getParent())->isLoopInvariant(Phi)) {
                                    dbgs() << "switching phis\n";
                                    roundInsts.clear();
                                    for(auto q : Insts[lindex]) roundInsts.insert (q);
                                    Phi = phi;
                                    found = true;
                                } else {
                                    assert(0);
                                }
                            }
                        } else {
                            for(auto q : Insts[lindex]) roundInsts.insert (q);
                            Phi = phi;
                            found = true;
                        }
				
			}
        
				
        
			}
            else if(Instruction* k = dyn_cast<Instruction>(v->get())) {

                if(!((!p) || L != nullptr)) continue;

                Instruction* j = k;

                Loop* L = LI.getLoopFor(j->getParent());
                if(L) {

                    SmallVector<Instruction*,8> Instrz;



                    if(p) {
                        dbgs() << "Non-loop-induction phi node! " << *p << "\n";
                        j = nullptr;
                        if(!getOddPhiFirst(L,p)) {
                            return false;
                        }
                        j = dyn_cast<Instruction> (getOddPhiFirst(L,p));
                        if(!j) {
                            return false;
                        }
                        Instrz.push_back(k);
                        Instrz.push_back(j);
                        L = LI.getLoopFor(j->getParent());

                    } else Instrz.push_back(k);




                    Instruction * phi = nullptr;
                    if(depthFirstSearch(j,LI,phi, Instrz, Loads, Phis, Insts)) {
                        if(Phi) {
                            if(Phi == phi) {
                                //add this
                                for(auto q : Instrz) roundInsts.insert (q);
                                found = true; //should have been before anyway
                            } else {
                                //check which is older.
                                if(LI.getLoopFor(Phi->getParent())->isLoopInvariant(phi)) {
                                    //do nothing
                                    dbgs() << "not switching phis\n";
                                } else if (LI.getLoopFor(phi->getParent())->isLoopInvariant(Phi)) {
                                    dbgs() << "switching phis\n";
                                    roundInsts.clear();
                                    for(auto q : Instrz) roundInsts.insert (q);
                                    Phi = phi;
                                    found = true;
                                } else {
                                    assert(0);
                                }
                            }
                        } else {
                            for(auto q : Instrz) roundInsts.insert (q);
                            Phi = phi;
                            found = true;
                        }
                    }
                }
            }
        }


        if(found) for(auto q : roundInsts) Instrs.push_back(q);

        return found;
    }



    bool runOnFunction(Function &F) override {



        LoopInfo &LI = getAnalysis<LoopInfoWrapperPass>().getLoopInfo();

        bool modified = false;

        SmallVector<Instruction*,4> Loads;
        SmallVector<Instruction*,4> Phis;
        SmallVector<int,4> Offsets;
        SmallVector<int,4> MaxOffsets;
        std::vector<SmallVector<Instruction*,8>> Insts;

        for(auto &BB : F) {



            for (auto &I : BB) {
                if (LoadInst *i = dyn_cast<LoadInst>(&I)) {
                    if(LI.getLoopFor(&BB)) {
                        SmallVector<Instruction*,8> Instrz;
                        Instrz.push_back(i);
                        Instruction * phi = nullptr;
                        if(depthFirstSearch(i,LI,phi,Instrz,  Loads, Phis, Insts)) {

                            int loads = 0;
                            for(auto &z : Instrz) {
                                if(dyn_cast<LoadInst>(z)) {
                                    loads++;
                                }
                            }

                            if(loads < 2) {
                                dbgs()<<"stride\n";    //don't remove the stride cases yet though. Only remove them once we know it's not in a sequence with an indirect.
#ifdef NO_STRIDES
                                //add a continue in here to avoid generating strided prefetches. Make sure to reduce the value of C accordingly!
                                continue;
#endif
                            }

                            dbgs() << "Can prefetch " << *i << " from PhiNode " << *phi << "\n";
                            dbgs() << "need to change \n";
                            for (auto &z : Instrz) {
                                dbgs() << *z << "\n";
                            }

                            Loads.push_back(i);
                            Insts.push_back(Instrz);
                            Phis.push_back(phi);
                            Offsets.push_back(0);
                            MaxOffsets.push_back(1);

                        }
                        else {
                            dbgs() << "Can't prefetch load" << *i << "\n";
                        }

                    }
                }
            }


        }

        for(uint64_t x=0; x<Loads.size(); x++) {
            ValueMap<Instruction*, Value*> Transforms;

            bool ignore = true;

            Loop* L = LI.getLoopFor(Phis[x]->getParent());
            if(!getCanonicalishSizeVariable(L)) continue;

            for(uint64_t y=x+1; y< Loads.size(); y++) {
                bool subset = true;
                for(auto &in : Insts[x]) {
                    if(std::find(Insts[y].begin(),Insts[y].end(),in) == Insts[y].end()) subset = false;
                }
                if(subset) {
                    MaxOffsets[x]++;
                    Offsets[y]++;
                    ignore=false;
                }
            }

            int loads = 0;

            for(auto &z : Insts[x]) {
                if(dyn_cast<LoadInst>(z)) {
                    loads++;
                }
            }


            if(loads < 2 && ignore) {
                dbgs() << "Ignoring" << *(Loads[x]) << "\n";
                continue; //remove strides with no dependent indirects.
            }


            IRBuilder<> Builder(Loads[x]);

            bool tryToPushDown = (LI.getLoopFor(Loads[x]->getParent()) != LI.getLoopFor(Phis[x]->getParent()));

            if(tryToPushDown) dbgs() << "Trying to push down!\n";



            //reverse list.
            SmallVector<Instruction*,8> newInsts;
            for(auto q = Insts[x].end()-1; q > Insts[x].begin()-1; q--) newInsts.push_back(*q);
            for(auto &z : newInsts) {
                if(Transforms.count(z)) continue;



                if(z == Phis[x]) {

                    Instruction* n;

                    bool weird = false;

                    Loop* L = LI.getLoopFor(Phis[x]->getParent());

                    int offset = (C_CONSTANT*MaxOffsets[x])/(MaxOffsets[x]+Offsets[x]);

                    if(z == getCanonicalishInductionVariable(L)) n = dyn_cast<Instruction>(Builder.CreateAdd(Phis[x],Phis[x]->getType()->isIntegerTy(64) ? ConstantInt::get(Type::getInt64Ty(M->getContext()),offset) : ConstantInt::get(Type::getInt32Ty(M->getContext()),offset)));
                    else if (z == getWeirdCanonicalishInductionVariable(L)) {
						//This covers code where a pointer is incremented, instead of a canonical induction variable.

                        n = getWeirdCanonicalishInductionVariableGep(L)->clone();
                        Builder.Insert(n);
                        n->setOperand (n->getNumOperands ()-1, ConstantInt::get(Type::getInt64Ty(M->getContext()),offset));
                        weird = true;

                        bool changed = true;
                        while(LI.getLoopFor(Phis[x]->getParent()) != LI.getLoopFor(n->getParent()) && changed) {

                            Loop* ol = LI.getLoopFor(n->getParent());

                            makeLoopInvariantSpec(n,changed,LI.getLoopFor(n->getParent()));

                            if(ol && ol == LI.getLoopFor(n->getParent())) break;


                        }

                    }




                    assert(L);
                    assert(n);

                    Value* size = getCanonicalishSizeVariable(L);
                    assert(size);
                    assert(size->getType()->isIntegerTy());
                    if(loads< 2 || !size || !size->getType()->isIntegerTy()) {
                        Transforms.insert(std::pair<Instruction*,Instruction*>(z,n));
                        continue;
                    }


                    Instruction* mod;

                    if(weird) {
						//This covers code where a pointer is incremented, instead of a canonical induction variable.

                        Instruction* endcast = dyn_cast<Instruction>(Builder.CreatePtrToInt(size,Type::getInt64Ty(M->getContext())));


                        Instruction* startcast =  dyn_cast<Instruction>(Builder.CreatePtrToInt(getWeirdCanonicalishInductionVariableFirst(L),Type::getInt64Ty(M->getContext())));


                        Instruction* valcast =  dyn_cast<Instruction>(Builder.CreatePtrToInt(n,Type::getInt64Ty(M->getContext())));


                        Instruction* sub1 = dyn_cast<Instruction>(Builder.CreateSub(valcast,startcast));
                        Instruction* sub2 = dyn_cast<Instruction>(Builder.CreateSub(endcast,startcast));

                        Value* cmp = Builder.CreateICmp(CmpInst::ICMP_SLT,sub1,sub2);
                        Instruction* rem = dyn_cast<Instruction>(Builder.CreateSelect(cmp,sub1,sub2));

                        Instruction* add = dyn_cast<Instruction>(Builder.CreateAdd(rem,startcast));

                        mod = dyn_cast<Instruction>(Builder.CreateIntToPtr(add,n->getType()));






                    }
                    else if(size->getType() != n->getType()) {
                        Instruction* cast = CastInst::CreateIntegerCast(size,n->getType(),true);
                        assert(cast);
                        Builder.Insert(cast);
                        Value* sub = Builder.CreateSub(cast,ConstantInt::get(Type::getInt64Ty(M->getContext()),1));
                        Value* cmp = Builder.CreateICmp(CmpInst::ICMP_SLT,sub,n);
                        mod = dyn_cast<Instruction>(Builder.CreateSelect(cmp,sub,n));

                    } else {

                        Value* sub = Builder.CreateSub(size,ConstantInt::get(n->getType(),1));
                        Value* cmp = Builder.CreateICmp(CmpInst::ICMP_SLT,sub,n);
                        mod = dyn_cast<Instruction>(Builder.CreateSelect(cmp,sub,n));
                    }


                    bool changed = true;
                    while(LI.getLoopFor(Phis[x]->getParent()) != LI.getLoopFor(mod->getParent()) && changed) {
                        Loop* ol = LI.getLoopFor(mod->getParent());
                        makeLoopInvariantSpec(mod,changed,LI.getLoopFor(mod->getParent()));
                        if(ol && ol == LI.getLoopFor(mod->getParent())) break;
                    }

                    Transforms.insert(std::pair<Instruction*,Instruction*>(z,mod));
                    modified = true;
                } else if (z == Loads[x]) {

                    Function *fun = Intrinsic::getDeclaration(F.getParent(), Intrinsic::prefetch);

                    assert(fun);

                    Instruction* oldGep = dyn_cast<Instruction>(Loads[x]->getOperand(0));
                    assert(oldGep);

                    Instruction* gep = dyn_cast<Instruction>(Transforms.lookup(oldGep));
                    assert(gep);
                    modified = true;



                    Instruction* cast = dyn_cast<Instruction>(Builder.CreateBitCast (gep, Type::getInt8PtrTy(M->getContext())));

                    bool changed = true;
                    while(LI.getLoopFor(Phis[x]->getParent()) != LI.getLoopFor(cast->getParent()) && changed) {
                        Loop* ol = LI.getLoopFor(cast->getParent());
                        makeLoopInvariantSpec(cast,changed,ol);
                        if(ol && ol == LI.getLoopFor(cast->getParent())) break;
                    }


                    Value* ar[] = {
                        cast,
                        ConstantInt::get(Type::getInt32Ty(M->getContext()),0),
                        ConstantInt::get(Type::getInt32Ty(M->getContext()),3),
                        ConstantInt::get(Type::getInt32Ty(M->getContext()),1)
                    };




                    CallInst* call = CallInst::Create(fun,ar);

                    call->insertBefore(cast->getParent()->getTerminator());





                } else if(PHINode * pn = dyn_cast<PHINode>(z)) {

                    Value* v = getOddPhiFirst(LI.getLoopFor(pn->getParent()),pn);
                    if(Instruction* ins = dyn_cast<Instruction>(v)) v = Transforms.lookup(ins);
                    Transforms.insert(std::pair<Instruction*,Value*>(z,v));
                }
                else {

                    Instruction* n = z->clone();

                    Use* u = n->getOperandList();
                    int64_t size = n->getNumOperands();
                    for(int64_t x = 0; x<size; x++) {
                        Value* v = u[x].get();
                        if(Instruction* t = dyn_cast<Instruction>(v)) {
                            if(Transforms.count(t)) {
                                n->setOperand(x,Transforms.lookup(t));
                            }
                        }
                    }

                    n->insertBefore(Loads[x]);

                    bool changed = true;
                    while(changed && LI.getLoopFor(Phis[x]->getParent()) != LI.getLoopFor(n->getParent())) {
                        changed = false;

                        makeLoopInvariantSpec(n,changed,LI.getLoopFor(n->getParent()));
                        if(changed) dbgs()<< "moved loop" << *n << "\n";
                        else dbgs()<< "not moved loop" << *n << "\n";

                    }

                    Transforms.insert(std::pair<Instruction*,Instruction*>(z,n));
                    modified = true;
                }

            }


        }

        return modified;
    }

};


char SwPrefetchPass::ID;



/// This function is called by the PassManagerBuilder to add the pass to the
/// pass manager.  You can query the builder for the optimisation level and so
/// on to decide whether to insert the pass.
void addSwPrefetchPass(const PassManagerBuilder &Builder, legacy::PassManagerBase &PM) {
    PM.add(createLoopRerollPass());
    PM.add(new SwPrefetchPass());
    PM.add(createVerifierPass());

}

/// Register the pass with the pass manager builder.  This instructs the
/// builder to call the `addSimplePass` function at the end of adding other
/// optimisations, so that we can insert the pass.  See the
/// `PassManagerBuilder` documentation for other extension points.
RegisterStandardPasses S(PassManagerBuilder::EP_VectorizerStart    ,
                         addSwPrefetchPass);


}
