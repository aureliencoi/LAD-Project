import { Component, OnInit } from '@angular/core';
import { MediaService, Movie, TvShow } from '../../core/services/media';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // <-- 1. AJOUTER CET IMPORT

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,   // Fournit *ngFor et *ngIf
    RouterModule    // <-- 2. AJOUTER CECI pour fournir [routerLink]
  ],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home implements OnInit {
  movies: Movie[] = [];
  series: TvShow[] = [];

  constructor(private mediaService: MediaService) {}

  ngOnInit(): void {
    this.mediaService.getMovies().subscribe({
      next: (data) => this.movies = data,
      error: (err) => console.error('Erreur lors de la récupération des films:', err)
    });

    this.mediaService.getSeries().subscribe({
      next: (data) => this.series = data,
      error: (err) => console.error('Erreur lors de la récupération des séries:', err)
    });
  }
}