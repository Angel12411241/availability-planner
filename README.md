## Команда за тестовете:
python -m pytest -v tst/e2e_tests.py

## Подход и сложност:
My approach to the task was to divide it into smaller problems. The first problem I wanted to take care of was to nomalize of the intervals.
I wanted sorted, non-overlapping intervals. After I achieved that the rest of the task became much simpler. I believe I managed to break down the task well 
thus the overall complexity of it was relatively low. The task itself carries similarities to leetcode problems. For example the normalization of the intervals is quite similar to one particular leetcode problem. 

The architecture of classes and modules is mostly to improve readability and make it easier for myself to do the development and solve the task.
Were it a real application that can be extended and new features are going to be added the architecture would be different.

## Отделено време:
The overall time I took for the task is around 3-4 hours. 

## Eвентуални пропуски:
I've treated this as mostly a task, similar to a leetcode problem. In production things like pydantic validation can be added to the interfaces. Furthermore code coverage needs to be improved and unittests written(right now I have e2e tests). For example at ASML we aim for 100% unittest code coverage, which I believe that for a big system that must be stable is reasonable(I am not saying that 100% code coverage means good testing). In this case I've added only the most important end to end tests. 
There are also bad inputs that I have not accounted for. Example: - work interval: (10,50), busy interval:(30,70).
This is something that in my opinion needs to raise an immediate failure, as it is illogical to be busy outside of a working window, thus maybe something else is wrong in earlier parts of the application if we are getting this data. This can be implemented as a check in the constructor of the ResourceCalendar. It is ofcourse possible to handle it as part of the normalization process and if a busy interval is going past working interval we can shorten it to fit in the working one that is part of. This can also be done when we are computing intersections to save compute time.

## Какъв проблем възниква, ако двама клиенти едновременно резервират предложения интервал; как би предотвратил двойна резервация и кога би инвалидирал кеш на наличностите:
Furthermore, in a real production environment, we need to consider concurrent operations; for example, what happens if two users try to reserve the same interval simultaneously. This can result in double booking, and one option is to allow it and use reconciliation jobs to notify one of the clients that their reservation is invalid, although this provides a poor client experience. The advantage of this approach is that it is simpler to implement and keeps the complexity of the application code, such as find_availability, low. In my opinion, a better approach is to use locking, where the resources being reserved, such as a machine and sensor, are locked before the reservation is made. To prevent deadlocks, locks should be acquired deterministically, for example in ascending alphabetical order, and released in descending order. This approach will naturally reduce application availability and increase latency, but for this business case I believe this is a worthwhile trade-off. If we had a database, we could choose between optimistic and pessimistic locking; if conflicts are rare, optimistic locking would reduce lock contention, while frequent conflicts would make pessimistic locking more suitable. In general, I would aim to use an atomic update with resource IDs if possible, although the exact approach would depend on the system setup and frontend.

## AI е използван за:
Development of the tests. I do belive that with the clear Specification that was provided to me AI would do an amazing job(probably better than I did) solving the task with a little bit of navigation, but due to the fact of this being an assesment I have not used it much(at all for the actual application code).