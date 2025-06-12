import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Interface pour typer un template
export interface Template {
  id: number;
  name: string;
  template_data: string; // Le JSON du canvas est une chaîne de caractères
  owner_id: number;
}

@Injectable({
  providedIn: 'root'
})
export class TemplatesService {
  private backendUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  /**
   * Envoie les données d'un nouveau template au backend.
   * @param name Le nom du template.
   * @param templateData Le JSON du canvas.
   */
  createTemplate(name: string, templateData: string): Observable<Template> {
    const body = {
      name: name,
      template_data: templateData
    };
    return this.http.post<Template>(`${this.backendUrl}/api/templates`, body);
  }

  /**
   * Récupère tous les templates de l'utilisateur.
   */
  getTemplates(): Observable<Template[]> {
    return this.http.get<Template[]>(`${this.backendUrl}/api/templates`);
  }
}
