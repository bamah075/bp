export interface User {
  id: string;
  email: string;
  password_hash: string;
  full_name: string;
  avatar_url?: string;
  role: 'admin' | 'manager' | 'member';
  status: 'active' | 'inactive';
  created_at: Date;
  updated_at: Date;
}

export interface Team {
  id: string;
  name: string;
  description?: string;
  owner_id: string;
  created_at: Date;
  updated_at: Date;
}

export interface TeamMember {
  id: string;
  team_id: string;
  user_id: string;
  role: 'member' | 'lead' | 'manager';
  joined_at: Date;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  team_id: string;
  owner_id: string;
  status: 'active' | 'archived' | 'completed';
  visibility: 'private' | 'team' | 'public';
  start_date?: Date;
  end_date?: Date;
  created_at: Date;
  updated_at: Date;
}

export interface Task {
  id: string;
  project_id: string;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'in_review' | 'done' | 'blocked';
  priority: 'low' | 'medium' | 'high' | 'critical';
  assignee_id?: string;
  due_date?: Date;
  start_date?: Date;
  estimated_duration?: number;
  actual_duration?: number;
  parent_task_id?: string;
  task_order?: number;
  created_at: Date;
  updated_at: Date;
  completed_at?: Date;
  created_by: string;
}

export interface TaskAssignee {
  id: string;
  task_id: string;
  user_id: string;
  assigned_at: Date;
}

export interface TaskDependency {
  id: string;
  task_id: string;
  depends_on_task_id: string;
  dependency_type: 'blocks' | 'blocked_by' | 'related_to';
}

export interface Comment {
  id: string;
  task_id: string;
  user_id: string;
  content: string;
  created_at: Date;
  updated_at: Date;
}

export interface CommentReply {
  id: string;
  comment_id: string;
  user_id: string;
  content: string;
  created_at: Date;
  updated_at: Date;
}

export interface Activity {
  id: string;
  user_id: string;
  entity_type: 'task' | 'project' | 'comment' | 'assignment';
  entity_id: string;
  action: 'created' | 'updated' | 'deleted' | 'commented' | 'assigned';
  changes?: Record<string, any>;
  created_at: Date;
  project_id?: string;
}

export interface Notification {
  id: string;
  user_id: string;
  actor_id?: string;
  type: 'task_assigned' | 'task_completed' | 'comment_added' | 'deadline_approaching' | 'status_changed';
  reference_type?: 'task' | 'comment' | 'project';
  reference_id?: string;
  read_at?: Date;
  created_at: Date;
}

export interface Session {
  id: string;
  user_id: string;
  token: string;
  expires_at: Date;
  created_at: Date;
}
