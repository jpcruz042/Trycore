import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Activity, ActivityDraft, Project, ProjectEvm } from './models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8001';

  listProjects(): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.apiUrl}/projects`);
  }

  createProject(payload: Partial<Project>): Observable<Project> {
    return this.http.post<Project>(`${this.apiUrl}/projects`, payload);
  }

  updateProject(projectId: string, payload: Partial<Project>): Observable<Project> {
    return this.http.put<Project>(`${this.apiUrl}/projects/${projectId}`, payload);
  }

  deleteProject(projectId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/projects/${projectId}`);
  }

  getProjectEvm(projectId: string): Observable<ProjectEvm> {
    return this.http.get<ProjectEvm>(`${this.apiUrl}/projects/${projectId}/evm`);
  }

  createActivity(projectId: string, payload: ActivityDraft): Observable<Activity> {
    return this.http.post<Activity>(`${this.apiUrl}/projects/${projectId}/activities`, payload);
  }

  updateActivity(projectId: string, activityId: string, payload: Partial<ActivityDraft>): Observable<Activity> {
    return this.http.put<Activity>(`${this.apiUrl}/projects/${projectId}/activities/${activityId}`, payload);
  }

  deleteActivity(projectId: string, activityId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/projects/${projectId}/activities/${activityId}`);
  }
}
