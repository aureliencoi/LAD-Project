import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import * as fabric from 'fabric';

// --- UTILISATION DE L'ALIAS DE CHEMIN ---
import { MediaService, MediaDetailData } from '@app/core/services/media';
// --- CORRECTION FINALE ET DÉFINITIVE APPLIQUÉE ---
import { LanguageFilterPipe } from '@app/core/pipes/language-filter-pipe';

@Component({
  selector: 'app-media-detail',
  standalone: true,
  imports: [
    CommonModule,
    LanguageFilterPipe
  ],
  templateUrl: './media-detail.html',
  styleUrl: './media-detail.scss'
})
export class MediaDetail implements OnInit, AfterViewInit {
  media: MediaDetailData | null = null;
  isLoading = true;
  errorMessage = '';
  public selectedLanguage: string = 'all';
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

  async setBackgroundImage(url: string): Promise<void> {
    try {
      const img = await fabric.Image.fromURL(url, { crossOrigin: 'anonymous' });
      img.scaleToWidth(this.canvas.width!);
      img.scaleToHeight(this.canvas.height!);
      this.canvas.backgroundImage = img;
      this.canvas.renderAll();
    } catch (error) {
      console.error("Erreur lors du chargement de l'image de fond :", error);
    }
  }

  handleFileUpload(event: any): void {
    const file = event.target.files[0];
    if (!file) { return; }
    const reader = new FileReader();
    reader.onload = (e) => {
      const imageUrl = e.target?.result as string;
      this.setBackgroundImage(imageUrl);
    };
    reader.readAsDataURL(file);
  }

  async addBadgeToCanvas(imageUrl: string): Promise<void> {
    try {
      const img = await fabric.Image.fromURL(imageUrl, { crossOrigin: 'anonymous' });
      
      img.scale(0.2);
      img.set({
        left: 50,
        top: 50
      });

      this.canvas.add(img);
      this.canvas.setActiveObject(img);
      this.canvas.renderAll();
    } catch (error) {
      console.error("Erreur lors de l'ajout du badge :", error);
    }
  }

  setLanguageFilter(lang: string): void {
    this.selectedLanguage = lang;
  }
}
