import { Component } from '@angular/core';
import { Renderer2, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Zero-TOTP Admin';
  constructor(private renderer: Renderer2, @Inject(DOCUMENT) private document: Document) { }

  // This function should be called after the external library has added the script to the head section
  addNonceToDynamicallyAddedScripts() {
    const scripts = this.document.querySelectorAll('script');
    
    scripts.forEach(script => {
      // Check if the script is dynamically added by the external library
      if (!script.hasAttribute('nonce')) {
        // Add the nonce attribute
        this.renderer.setAttribute(script, 'nonce', 'random-nonce-placeholder'); 
      }
    });
  }


}
