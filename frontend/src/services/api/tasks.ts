import { apiClient } from './client';

export interface Task {
  id: string;
  project_id: string;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'in_review' | 'done' | 'blocked';
  priority: 'low' | 'medium' | 'high' | 'critical';
  assignee_id?: string;
  due_date?: string;
  start_date?: string;
  estimated_duration?: number;
  actual_duration?: number;
  parent_task_id?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface CreateTaskRequest {
  project_id: string;
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high' | 'critical';
  assignee_id?: string;
  due_date?: string;
  parent_task_id?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: 'todo' | 'in_progress' | 'in_review' | 'done' | 'blocked';
  priority?: 'low' | 'medium' | 'high' | 'critical';
  assignee_id?: string;
  due_date?: string;
}

export interface TaskListResponse {
  data: Task[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
}

export const tasksApi = {
  createTask: async (data: CreateTaskRequest): Promise<Task> => {
    const response = await apiClient.post<Task>('/tasks', data);
    return response.data;
  },

  getTask: async (id: string): Promise<Task> => {
    const response = await apiClient.get<Task>(`/tasks/${id}`);
    return response.data;
  },

  listTasks: async (projectId?: string, page = 1, limit = 50): Promise<TaskListResponse> => {
    const params = new URLSearchParams();
    if (projectId) params.append('project_id', projectId);
    params.append('page', page.toString());
    params.append('limit', limit.toString());

    const response = await apiClient.get<TaskListResponse>(
      `/tasks?${params.toString()}`
    );
    return response.data;
  },

  updateTask: async (id: string, data: UpdateTaskRequest): Promise<Task> => {
    const response = await apiClient.patch<Task>(`/tasks/${id}`, data);
    return response.data;
  },

  deleteTask: async (id: string): Promise<void> => {
    await apiClient.delete(`/tasks/${id}`);
  },

  updateTaskStatus: async (
    id: string,
    status: 'todo' | 'in_progress' | 'in_review' | 'done' | 'blocked'
  ): Promise<Task> => {
    const response = await apiClient.patch<Task>(`/tasks/${id}/status`, { status });
    return response.data;
  },

  assignTask: async (id: string, userId: string): Promise<Task> => {
    const response = await apiClient.post<Task>(`/tasks/${id}/assign`, { userId });
    return response.data;
  },

  unassignTask: async (id: string, userId: string): Promise<Task> => {
    const response = await apiClient.delete<Task>(`/tasks/${id}/assign/${userId}`);
    return response.data;
  },
};
