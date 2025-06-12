import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import * as fabric from 'fabric';

// Imports pour le Drag and Drop
import { CdkDrag, CdkDropList, CdkDropListGroup, CdkDragDrop } from '@angular/cdk/drag-drop';

import { MediaService, MediaDetailData } from '@app/core/services/media';
import { LanguageFilterPipe } from '@app/core/pipes/language-filter-pipe';
import { AssetsService, Badge } from '@app/core/services/assets.service';
import { TemplatesService } from '@app/core/services/templates.service';

@Component({
  selector: 'app-media-detail',
  standalone: true,
  imports: [
    CommonModule,
    LanguageFilterPipe,
    CdkDropList,
    CdkDrag,
    CdkDropListGroup
  ],
  templateUrl: './media-detail.html',
  styleUrl: './media-detail.scss'
})
export class MediaDetail implements OnInit {
  @ViewChild('assetCanvasElement') canvasRef!: ElementRef<HTMLCanvasElement>;
  
  media: MediaDetailData | null = null;
  isLoading = true;
  errorMessage = '';
  public selectedLanguage: string = 'all';
  public availableBadges: Badge[] = [];
  public pageBackgroundUrl: string | null = null;
  private canvas!: fabric.Canvas;

  constructor(
    private route: ActivatedRoute,
    private mediaService: MediaService,
    private assetsService: AssetsService,
    private templatesService: TemplatesService,
  ) {}

  ngOnInit(): void {
    this.loadMediaDetails();
    this.loadBadges();
  }
  
  loadMediaDetails(): void {
    const type = this.route.snapshot.paramMap.get('type');
    const id = Number(this.route.snapshot.paramMap.get('id'));

    if (type === 'movie' && id) {
      this.mediaService.getMovieDetail(id).subscribe({
        next: (data) => { 
          this.media = data; 
          this.isLoading = false;
          if (data.tmdb_images?.backdrops && data.tmdb_images.backdrops.length > 0) {
            this.pageBackgroundUrl = 'https://image.tmdb.org/t/p/original' + data.tmdb_images.backdrops[0].file_path;
          }
          this.initCanvas();
        },
        error: (err) => { this.errorMessage = "Erreur lors de la récupération des détails du film."; this.isLoading = false; }
      });
    }
  }

  loadBadges(): void {
    this.assetsService.getCustomBadges().subscribe(customBadges => {
      this.availableBadges = customBadges;
    });
  }
  
  handleBadgeUpload(event: any): void {
    const file: File = event.target.files[0];
    if (!file) { return; }
    this.assetsService.uploadBadge(file).subscribe({
      next: (newBadge) => { this.availableBadges.push(newBadge); event.target.value = null; },
      error: (err) => { console.error("Erreur lors de l'upload du badge:", err); this.errorMessage = err.error.detail || "Une erreur est survenue lors de l'upload."; }
    });
  }

  initCanvas(): void {
    setTimeout(() => {
      if (this.canvasRef) {
        const canvasEl = this.canvasRef.nativeElement;
        const container = canvasEl.parentElement!;
        
        this.canvas = new fabric.Canvas(canvasEl, {
          width: container.clientWidth,
          height: container.clientHeight
        });
        this.canvas.backgroundColor = 'rgba(51, 51, 51, 0.7)';
        this.canvas.renderAll();
      }
    }, 0);
  }
  
  drop(event: CdkDragDrop<any>): void {
    const droppedData = event.item.data;
    
    if (droppedData.type === 'background') {
      this.setBackgroundImage(droppedData.url);
    } else if (droppedData.type === 'badge') {
      const canvasRect = this.canvas.getElement().getBoundingClientRect();
      const dropPoint = event.dropPoint;
      const x = dropPoint.x - canvasRect.left;
      const y = dropPoint.y - canvasRect.top;
      this.addBadgeToCanvas(droppedData.path, x, y);
    }
  }

  async setBackgroundImage(url: string): Promise<void> {
    if (!this.canvas) return;
    try {
      const img = await fabric.Image.fromURL(url, { crossOrigin: 'anonymous' });
      this.canvas.backgroundImage = img;
      this.canvas.backgroundImage?.scaleToWidth(this.canvas.width || 0);
      this.canvas.backgroundImage?.scaleToHeight(this.canvas.height || 0);
      this.canvas.renderAll();
    } catch (error) {
      console.error("Erreur dans setBackgroundImage :", error);
    }
  }

  async addBadgeToCanvas(imageUrl: string, x: number, y: number): Promise<void> {
    if (!this.canvas) return;
    const fullUrl = `http://127.0.0.1:8000${imageUrl}`;
    try {
      const img = await fabric.Image.fromURL(fullUrl, { crossOrigin: 'anonymous' });
      img.scale(0.2);
      
      // On positionne le badge là où il a été déposé
      img.set({
        left: x - img.getScaledWidth() / 2,
        top: y - img.getScaledHeight() / 2,
      });

      this.canvas.add(img);
      this.canvas.setActiveObject(img);
      this.canvas.renderAll();
    } catch (error) {
      console.error("Erreur dans addBadgeToCanvas :", error);
    }
  }

  setLanguageFilter(lang: string): void {
    this.selectedLanguage = lang;
  }

  saveAsTemplate(): void {
    // ... (la logique de sauvegarde reste la même)
  }
}