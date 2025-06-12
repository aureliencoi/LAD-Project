import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Interface pour typer nos objets 'badge'
export interface Badge {
  name: string;
  path: string;
}

@Injectable({
  providedIn: 'root'
})
export class AssetsService {
  private backendUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  /**
   * Récupère la liste des badges personnalisés de l'utilisateur.
   */
  getCustomBadges(): Observable<Badge[]> {
    return this.http.get<Badge[]>(`${this.backendUrl}/api/badges`);
  }

  /**
   * Envoie un fichier de badge au backend pour le sauvegarder.
   * @param file Le fichier image à uploader.
   */
  uploadBadge(file: File): Observable<Badge> {
    const formData = new FormData();
    formData.append('file', file, file.name);
    
    // HttpClient s'occupe de mettre le bon Content-Type pour le multipart/form-data
    return this.http.post<Badge>(`${this.backendUrl}/api/badges`, formData);
  }
}
