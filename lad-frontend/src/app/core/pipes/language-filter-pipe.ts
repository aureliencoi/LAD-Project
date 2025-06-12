import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'languageFilter',
  standalone: true
})
export class LanguageFilterPipe implements PipeTransform {

  transform(items: any[] | undefined | null, language: string): any[] {
    // Si la liste d'items est vide ou nulle, on ne fait rien
    if (!items) {
      return [];
    }
    
    // Si l'utilisateur veut voir toutes les images, on retourne la liste complète
    if (language === 'all') {
      return items;
    }
    
    // Si l'utilisateur veut les images sans texte (le code langue est 'null' sur TMDB)
    if (language === 'null') {
      return items.filter(item => item.iso_639_1 === null);
    }
    
    // Sinon, on filtre par le code de langue (ex: 'fr', 'en')
    return items.filter(item => item.iso_639_1 === language);
  }

}
