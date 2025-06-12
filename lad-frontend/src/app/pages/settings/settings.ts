import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './settings.html',
  styleUrl: './settings.scss'
})
export class Settings implements OnInit {
  tmdbApiKey = '';
  radarrUrl = '';
  radarrApiKey = '';
  sonarrUrl = '';
  sonarrApiKey = '';

  successMessage = '';
  private backendUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Charger les paramètres TMDB
    this.http.get<any>(`${this.backendUrl}/api/settings/tmdb`).subscribe({
      next: (data) => this.tmdbApiKey = data.api_key,
      error: (err) => console.log("Pas de paramètres TMDB existants.")
    });

    // Charger les paramètres Radarr
    this.http.get<any>(`${this.backendUrl}/api/settings/radarr`).subscribe({
      next: (data) => {
        this.radarrUrl = data.url;
        this.radarrApiKey = data.api_key;
      },
      error: (err) => console.log("Pas de paramètres Radarr existants.")
    });
    
    // Charger les paramètres Sonarr
    this.http.get<any>(`${this.backendUrl}/api/settings/sonarr`).subscribe({
      next: (data) => {
        this.sonarrUrl = data.url;
        this.sonarrApiKey = data.api_key;
      },
      error: (err) => console.log("Pas de paramètres Sonarr existants.")
    });
  }

  saveTmdbSettings(): void {
    const settings = { api_key: this.tmdbApiKey };
    this.http.post(`${this.backendUrl}/api/settings/tmdb`, settings).subscribe(() => {
      this.successMessage = 'Paramètres TMDB sauvegardés avec succès !';
      setTimeout(() => this.successMessage = '', 3000);
    });
  }

  saveRadarrSettings(): void {
    const settings = { url: this.radarrUrl, api_key: this.radarrApiKey };
    this.http.post(`${this.backendUrl}/api/settings/radarr`, settings).subscribe(() => {
      this.successMessage = 'Paramètres Radarr sauvegardés avec succès !';
      setTimeout(() => this.successMessage = '', 3000);
    });
  }

  saveSonarrSettings(): void {
    const settings = { url: this.sonarrUrl, api_key: this.sonarrApiKey };
    this.http.post(`${this.backendUrl}/api/settings/sonarr`, settings).subscribe(() => {
      this.successMessage = 'Paramètres Sonarr sauvegardés avec succès !';
      setTimeout(() => this.successMessage = '', 3000);
    });
  }
}