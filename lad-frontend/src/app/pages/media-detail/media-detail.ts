import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MediaService, MediaDetailData } from '../../core/services/media';
import { CommonModule } from '@angular/common';
import * as fabric from 'fabric';

@Component({
  selector: 'app-media-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './media-detail.html',
  styleUrl: './media-detail.scss'
})
export class MediaDetail implements OnInit, AfterViewInit {
  media: MediaDetailData | null = null;
  isLoading = true;
  errorMessage = '';

  private canvas!: fabric.Canvas;

  constructor(
    private route: ActivatedRoute,
    private mediaService: MediaService
  ) {}

  ngOnInit(): void {
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
      // logique pour les séries à venir
    } else {
      this.errorMessage = "Type de média ou ID invalide.";
      this.isLoading = false;
    }
  }

  ngAfterViewInit(): void {
    this.canvas = new fabric.Canvas('assetCanvas');
    this.canvas.backgroundColor = '#333';
    this.canvas.renderAll();
  }

  // --- FONCTION ENTIÈREMENT CORRIGÉE SELON L'ERREUR ---
  async setBackgroundImage(url: string): Promise<void> {
    try {
      const img = await fabric.Image.fromURL(url, { crossOrigin: 'anonymous' });

      // On met l'image à l'échelle pour qu'elle remplisse le canvas
      img.scaleToWidth(this.canvas.width!);
      img.scaleToHeight(this.canvas.height!);
      
      // --- CORRECTION DÉFINITIVE ---
      // On ASSIGNE l'image à la PROPRIÉTÉ 'backgroundImage'
      this.canvas.backgroundImage = img;
      
      // Et on demande au canvas de se redessiner pour afficher le résultat
      this.canvas.renderAll();

    } catch (error) {
      console.error("Erreur lors du chargement de l'image dans le canvas :", error);
      this.errorMessage = "Impossible de charger cette image.";
    }
  }

  handleFileUpload(event: any): void {
    const file = event.target.files[0];
    if (!file) {
      return;
    }
    const reader = new FileReader();

    reader.onload = (e) => {
      const imageUrl = e.target?.result as string;
      this.setBackgroundImage(imageUrl);
    };

    reader.readAsDataURL(file);
  }
}