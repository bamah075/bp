export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code?: string;
  };
  pagination?: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
}

export interface AuthPayload {
  email: string;
  password: string;
}

export interface TokenPayload {
  id: string;
  email: string;
  role: string;
  iat?: number;
  exp?: number;
}

export interface CreateUserRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
  team_id: string;
  visibility?: 'private' | 'team' | 'public';
  start_date?: Date;
  end_date?: Date;
}

export interface CreateTaskRequest {
  project_id: string;
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high' | 'critical';
  assignee_id?: string;
  due_date?: Date;
  parent_task_id?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: 'todo' | 'in_progress' | 'in_review' | 'done' | 'blocked';
  priority?: 'low' | 'medium' | 'high' | 'critical';
  assignee_id?: string;
  due_date?: Date;
}

export interface PaginationQuery {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface TaskFilter extends PaginationQuery {
  status?: string;
  priority?: string;
  assignee_id?: string;
  due_date_from?: Date;
  due_date_to?: Date;
  search?: string;
}
