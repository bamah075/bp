import { useState, useCallback } from 'react';
import { tasksApi, Task, CreateTaskRequest, UpdateTaskRequest } from '../services/api/tasks';

interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  loadTasks: (projectId?: string, page?: number) => Promise<void>;
  createTask: (data: CreateTaskRequest) => Promise<Task>;
  updateTask: (id: string, data: UpdateTaskRequest) => Promise<Task>;
  deleteTask: (id: string) => Promise<void>;
  updateTaskStatus: (id: string, status: Task['status']) => Promise<Task>;
  assignTask: (id: string, userId: string) => Promise<Task>;
  unassignTask: (id: string, userId: string) => Promise<Task>;
}

export const useTasks = (): UseTasksReturn => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = useCallback(
    async (projectId?: string, page = 1) => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await tasksApi.listTasks(projectId, page);
        setTasks(response.data);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load tasks';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const createTask = useCallback(async (data: CreateTaskRequest): Promise<Task> => {
    setError(null);
    try {
      const task = await tasksApi.createTask(data);
      setTasks((prev) => [task, ...prev]);
      return task;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create task';
      setError(message);
      throw err;
    }
  }, []);

  const updateTask = useCallback(
    async (id: string, data: UpdateTaskRequest): Promise<Task> => {
      setError(null);
      try {
        const task = await tasksApi.updateTask(id, data);
        setTasks((prev) =>
          prev.map((t) => (t.id === id ? task : t))
        );
        return task;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to update task';
        setError(message);
        throw err;
      }
    },
    []
  );

  const deleteTask = useCallback(async (id: string) => {
    setError(null);
    try {
      await tasksApi.deleteTask(id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete task';
      setError(message);
      throw err;
    }
  }, []);

  const updateTaskStatus = useCallback(
    async (id: string, status: Task['status']): Promise<Task> => {
      setError(null);
      try {
        const task = await tasksApi.updateTaskStatus(id, status);
        setTasks((prev) =>
          prev.map((t) => (t.id === id ? task : t))
        );
        return task;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to update status';
        setError(message);
        throw err;
      }
    },
    []
  );

  const assignTask = useCallback(
    async (id: string, userId: string): Promise<Task> => {
      setError(null);
      try {
        const task = await tasksApi.assignTask(id, userId);
        setTasks((prev) =>
          prev.map((t) => (t.id === id ? task : t))
        );
        return task;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to assign task';
        setError(message);
        throw err;
      }
    },
    []
  );

  const unassignTask = useCallback(
    async (id: string, userId: string): Promise<Task> => {
      setError(null);
      try {
        const task = await tasksApi.unassignTask(id, userId);
        setTasks((prev) =>
          prev.map((t) => (t.id === id ? task : t))
        );
        return task;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to unassign task';
        setError(message);
        throw err;
      }
    },
    []
  );

  return {
    tasks,
    isLoading,
    error,
    loadTasks,
    createTask,
    updateTask,
    deleteTask,
    updateTaskStatus,
    assignTask,
    unassignTask,
  };
};
