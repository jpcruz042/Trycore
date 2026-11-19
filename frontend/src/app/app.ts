import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

import { ApiService } from './api.service';
import { Activity, Project, ProjectEvm } from './models';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  private readonly api = inject(ApiService);

  readonly projects = signal<Project[]>([]);
  readonly selected = signal<ProjectEvm | null>(null);
  readonly loading = signal(false);
  readonly error = signal('');
  readonly showProjectForm = signal(false);
  readonly showActivityForm = signal(false);

  projectDraft = { name: '', description: '', cut_off_date: '' };
  activityDraft = {
    name: '',
    bac: 0,
    planned_progress: 0,
    actual_progress: 0,
    actual_cost: 0,
  };
  editingActivityId: string | null = null;

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.loading.set(true);
    this.error.set('');
    this.api.listProjects().subscribe({
      next: (projects) => {
        this.projects.set(projects);
        if (!this.selected() && projects.length > 0) {
          this.selectProject(projects[0].id);
        } else if (this.selected()) {
          this.selectProject(this.selected()?.id as string);
        }
        this.loading.set(false);
      },
      error: () => {
        this.error.set('No se pudo conectar con la API. Verifica que el backend esté activo.');
        this.loading.set(false);
      },
    });
  }

  selectProject(projectId: string): void {
    this.loading.set(true);
    this.api.getProjectEvm(projectId).subscribe({
      next: (project) => {
        this.selected.set(project);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar el proyecto seleccionado.');
        this.loading.set(false);
      },
    });
  }

  createProject(): void {
    if (!this.projectDraft.name.trim()) return;
    this.api.createProject(this.projectDraft).subscribe({
      next: (project) => {
        this.projectDraft = { name: '', description: '', cut_off_date: '' };
        this.showProjectForm.set(false);
        this.loadProjects();
        this.selectProject(project.id);
      },
      error: () => this.error.set('No se pudo crear el proyecto.'),
    });
  }

  deleteProject(): void {
    const project = this.selected();
    if (!project || !confirm(`¿Eliminar el proyecto "${project.name}" y sus actividades?`)) return;
    this.api.deleteProject(project.id).subscribe({
      next: () => {
        this.selected.set(null);
        this.loadProjects();
      },
      error: () => this.error.set('No se pudo eliminar el proyecto.'),
    });
  }

  startActivity(): void {
    this.editingActivityId = null;
    this.activityDraft = { name: '', bac: 0, planned_progress: 0, actual_progress: 0, actual_cost: 0 };
    this.showActivityForm.set(true);
  }

  editActivity(activity: Activity): void {
    this.editingActivityId = activity.id;
    this.activityDraft = {
      name: activity.name,
      bac: Number(activity.bac),
      planned_progress: Number(activity.planned_progress),
      actual_progress: Number(activity.actual_progress),
      actual_cost: Number(activity.actual_cost),
    };
    this.showActivityForm.set(true);
  }

  saveActivity(): void {
    const project = this.selected();
    if (!project || !this.activityDraft.name.trim()) return;

    const request = this.editingActivityId
      ? this.api.updateActivity(project.id, this.editingActivityId, this.activityDraft)
      : this.api.createActivity(project.id, this.activityDraft);

    request.subscribe({
      next: () => {
        this.showActivityForm.set(false);
        this.editingActivityId = null;
        this.selectProject(project.id);
      },
      error: () => this.error.set('No se pudo guardar la actividad.'),
    });
  }

  deleteActivity(activity: Activity): void {
    const project = this.selected();
    if (!project || !confirm(`¿Eliminar la actividad "${activity.name}"?`)) return;
    this.api.deleteActivity(project.id, activity.id).subscribe({
      next: () => this.selectProject(project.id),
      error: () => this.error.set('No se pudo eliminar la actividad.'),
    });
  }

  number(value: string | null | undefined): number {
    return value == null ? 0 : Number(value);
  }

  money(value: string | null | undefined): string {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(this.number(value));
  }

  statusLabel(status: string, kind: 'cost' | 'time'): string {
    const labels: Record<string, string> = {
      under_budget: 'Bajo presupuesto',
      over_budget: 'Sobre presupuesto',
      on_budget: 'En presupuesto',
      ahead: 'Adelantado',
      behind: 'Atrasado',
      on_schedule: 'En cronograma',
      not_available: 'Sin datos',
    };
    return labels[status] ?? 'Sin datos';
  }

  statusClass(status: string): string {
    if (['under_budget', 'ahead', 'on_budget', 'on_schedule'].includes(status)) return 'positive';
    if (['over_budget', 'behind'].includes(status)) return 'negative';
    return 'neutral';
  }

  chartMaximum(): number {
    const activities = this.selected()?.activities ?? [];
    return Math.max(1, ...activities.map((activity) =>
      Math.max(this.number(activity.pv), this.number(activity.ev), this.number(activity.actual_cost))
    ))
  }

  barWidth(value: string | null | undefined): number {
    return Math.round((this.number(value) / this.chartMaximum()) * 100);
  }
}
