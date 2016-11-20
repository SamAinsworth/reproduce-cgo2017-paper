/**
 * @file    task_queue.h
 * @author  Cagri Balkesen <cagri.balkesen@inf.ethz.ch>
 * @date    Sat Feb  4 20:00:58 2012
 * @version $Id: task_queue.h 3017 2012-12-07 10:56:20Z bcagri $
 * 
 * @brief  Implements task queue facility for the join processing.
 * 
 */
#ifndef TASK_QUEUE_H
#define TASK_QUEUE_H

#include <pthread.h>
#include <stdlib.h>

#include "types.h" /* relation_t, int32_t */

/** 
 * @defgroup TaskQueue Task Queue Implementation 
 * @{
 */

typedef struct task_t task_t;
typedef struct task_list_t task_list_t;
typedef struct task_queue_t task_queue_t;

struct task_t {
    relation_t relR;
    relation_t tmpR;
    relation_t relS;
    relation_t tmpS;
    task_t *   next;
};

struct task_list_t {
    task_t *      tasks;
    task_list_t * next;
    int           curr;
};

struct task_queue_t {
    pthread_mutex_t lock;
    pthread_mutex_t alloc_lock;
    task_t *        head;
    task_list_t *   free_list;
    int32_t         count;
    int32_t         alloc_size;
};

inline 
task_t * 
get_next_task(task_queue_t * tq) __attribute__((always_inline));

inline 
void 
add_tasks(task_queue_t * tq, task_t * t) __attribute__((always_inline));

inline 
task_t * 
get_next_task(task_queue_t * tq) 
{
    pthread_mutex_lock(&tq->lock);
    task_t * ret = 0;
    if(tq->count > 0){
        ret = tq->head;
        tq->head = ret->next;
        tq->count --;
    }
    pthread_mutex_unlock(&tq->lock);

    return ret;
}

inline 
void 
add_tasks(task_queue_t * tq, task_t * t) 
{
    pthread_mutex_lock(&tq->lock);
    t->next = tq->head;
    tq->head = t;
    tq->count ++;
    pthread_mutex_unlock(&tq->lock);
}

/* atomically get the next available task */
inline 
task_t * 
task_queue_get_atomic(task_queue_t * tq) __attribute__((always_inline));

/* atomically add a task */
inline 
void 
task_queue_add_atomic(task_queue_t * tq, task_t * t) 
    __attribute__((always_inline));

inline 
void 
task_queue_add(task_queue_t * tq, task_t * t) __attribute__((always_inline));

inline 
void 
task_queue_copy_atomic(task_queue_t * tq, task_t * t)
    __attribute__((always_inline));

/* get a free slot of task_t */
inline 
task_t * 
task_queue_get_slot_atomic(task_queue_t * tq) __attribute__((always_inline));

inline 
task_t * 
task_queue_get_slot(task_queue_t * tq) __attribute__((always_inline));

/* initialize a task queue with given allocation block size */
task_queue_t * 
task_queue_init(int alloc_size);

void 
task_queue_free(task_queue_t * tq);

/**************** DEFINITIONS ********************************************/

inline 
task_t * 
task_queue_get_atomic(task_queue_t * tq) 
{
    pthread_mutex_lock(&tq->lock);
    task_t * ret = 0;
    if(tq->count > 0){
        ret      = tq->head;
        tq->head = ret->next;
        tq->count --;
    }
    pthread_mutex_unlock(&tq->lock);

    return ret;
}

inline 
void 
task_queue_add_atomic(task_queue_t * tq, task_t * t) 
{
    pthread_mutex_lock(&tq->lock);
    t->next  = tq->head;
    tq->head = t;
    tq->count ++;
    pthread_mutex_unlock(&tq->lock);

}

inline 
void 
task_queue_add(task_queue_t * tq, task_t * t) 
{
    t->next  = tq->head;
    tq->head = t;
    tq->count ++;
}

/* sorted add 
inline 
void 
task_queue_add_atomic(task_queue_t * tq, task_t * t) 
{
    pthread_mutex_lock(&tq->lock);
    task_queue_add(tq, t);
    pthread_mutex_unlock(&tq->lock);

}

inline 
int32_t 
maxtuples(task_t * t) __attribute__((always_inline));

inline 
int32_t 
maxtuples(task_t * t)
{
    int32_t max = t->relS.num_tuples;
    if(t->relR.num_tuples > max)
        max = t->relR.num_tuples;

    return max;
}

inline 
void 
task_queue_add(task_queue_t * tq, task_t * t) 
{
    int32_t maxnew;

    if(tq->head == NULL ||
       ((maxnew = maxtuples(t)) >= maxtuples(tq->head))) {
        
        t->next  = tq->head;
        tq->head = t;
        tq->count ++;
        return;
        
    }

    task_t * prev, * curr;
    prev = tq->head;
    curr = tq->head->next;

    while(curr) {
        if(maxnew < maxtuples(curr)) {
            prev = curr;
            curr = curr->next;
        }
        else
            break;
    }

    if(curr) {
        t->next = curr->next;
        curr->next = t;
    }
    else {
        t->next = prev->next;
        prev->next = t;
    }

    tq->count ++;
    return;
}
*/

inline 
void 
task_queue_copy_atomic(task_queue_t * tq, task_t * t) 
{
    pthread_mutex_lock(&tq->lock);
    task_t * slot = task_queue_get_slot(tq);
    *slot = *t; /* copy */
    task_queue_add(tq, slot);
    pthread_mutex_unlock(&tq->lock);
}

inline 
task_t * 
task_queue_get_slot(task_queue_t * tq)
{
    task_list_t * l = tq->free_list;
    task_t * ret;
    if(l->curr < tq->alloc_size) {
        ret = &(l->tasks[l->curr]);
        l->curr++;
    }
    else {
        task_list_t * nl = (task_list_t*) malloc(sizeof(task_list_t));
        nl->tasks = (task_t*) malloc(tq->alloc_size * sizeof(task_t));
        nl->curr = 1;
        nl->next = tq->free_list;
        tq->free_list = nl;
        ret = &(nl->tasks[0]);
    }

    return ret;
}

/* get a free slot of task_t */
inline 
task_t * 
task_queue_get_slot_atomic(task_queue_t * tq)
{
    pthread_mutex_lock(&tq->alloc_lock);
    task_t * ret = task_queue_get_slot(tq);
    pthread_mutex_unlock(&tq->alloc_lock);

    return ret;
}

/* initialize a task queue with given allocation block size */
task_queue_t * 
task_queue_init(int alloc_size) 
{
    task_queue_t * ret = (task_queue_t*) malloc(sizeof(task_queue_t));
    ret->free_list = (task_list_t*) malloc(sizeof(task_list_t));
    ret->free_list->tasks = (task_t*) malloc(alloc_size * sizeof(task_t));
    ret->free_list->curr = 0;
    ret->free_list->next = NULL;
    ret->count      = 0;
    ret->alloc_size = alloc_size;
    ret->head       = NULL;
    pthread_mutex_init(&ret->lock, NULL);
    pthread_mutex_init(&ret->alloc_lock, NULL);

    return ret;
}

void 
task_queue_free(task_queue_t * tq) 
{
    task_list_t * tmp = tq->free_list;
    while(tmp) {
        free(tmp->tasks);
        task_list_t * tmp2 = tmp->next;
        free(tmp);
        tmp = tmp2;
    }
    free(tq);
}

/** @} */

#endif /* TASK_QUEUE_H */
