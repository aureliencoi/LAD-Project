import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Movie {
  id: number;
  title: string;
  year: number;
  poster_url: string;
}

export interface TvShow {
  id: number;
  title: string;
  year: number;
  poster_url: string;
}

// On utilise 'any' pour les détails car la structure est très riche
export type MediaDetailData = any;

@Injectable({
  providedIn: 'root'
})
export class MediaService {
  private backendUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  getMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.backendUrl}/api/movies`);
  }

  getSeries(): Observable<TvShow[]> {
    return this.http.get<TvShow[]>(`${this.backendUrl}/api/series`);
  }

  // --- NOUVELLES MÉTHODES ---
  getMovieDetail(id: number): Observable<MediaDetailData> {
    return this.http.get<MediaDetailData>(`${this.backendUrl}/api/movie/${id}`);
  }

  getSeriesDetail(id: number): Observable<MediaDetailData> {
    return this.http.get<MediaDetailData>(`${this.backendUrl}/api/series/${id}`);
  }
}