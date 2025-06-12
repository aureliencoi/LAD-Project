import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MediaService, MediaDetailData } from '../../core/services/media';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-media-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './media-detail.html',
  styleUrl: './media-detail.scss'
})
export class MediaDetail implements OnInit {
  media: MediaDetailData | null = null;
  isLoading = true;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private mediaService: MediaService
  ) {}

  ngOnInit(): void {
    // On récupère les paramètres de l'URL
    const type = this.route.snapshot.paramMap.get('type');
    const id = Number(this.route.snapshot.paramMap.get('id'));

    if (type === 'movie' && id) {
      this.mediaService.getMovieDetail(id).subscribe({
        next: (data) => {
          this.media = data;
          this.isLoading = false;
        },
        error: (err) => {
          this.errorMessage = "Erreur lors de la récupération des détails du film.";
          this.isLoading = false;
        }
      });
    } else if (type === 'series' && id) {
      this.mediaService.getSeriesDetail(id).subscribe({
        next: (data) => {
          this.media = data;
          this.isLoading = false;
        },
        error: (err) => {
          this.errorMessage = "Erreur lors de la récupération des détails de la série.";
          this.isLoading = false;
        }
      });
    } else {
      this.errorMessage = "Type de média ou ID invalide.";
      this.isLoading = false;
    }
  }
}