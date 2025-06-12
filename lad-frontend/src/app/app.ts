import { Component } from '@angular/core';
// --- CORRECTION : Importer RouterModule et RouterOutlet ici ---
import { RouterModule, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  // --- CORRECTION : Ajouter RouterModule aux imports ---
  imports: [RouterOutlet, RouterModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  title = 'lad-frontend';
}