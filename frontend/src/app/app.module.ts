import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { FooterComponent } from './footer/footer.component';
import { NavbarComponent } from './navbar/navbar.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { TranslateService, MissingTranslationHandler, MissingTranslationHandlerParams, } from '@ngx-translate/core';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { Utils } from './common/Utils/utils.service';
import { HttpClientModule,HttpClient } from '@angular/common/http';
import defaultLanguage from "./../assets/i18n/en-uk.json";
import { ToastrModule } from 'ngx-toastr';

export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http);
}

export class MissingTranslationHelper implements MissingTranslationHandler {
  handle(params: MissingTranslationHandlerParams) {
    return params.key;
  }
}


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    FooterComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FontAwesomeModule,
    FormsModule,
    ToastrModule.forRoot(),
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
          useFactory: HttpLoaderFactory,
          deps: [HttpClient],
      },
      missingTranslationHandler: {
        provide: MissingTranslationHandler,
        useClass: MissingTranslationHelper
      },
    }),
    HttpClientModule,
  ],
  providers: [Crypto, Utils],
  bootstrap: [AppComponent]
})
export class AppModule { 

  constructor(translate: TranslateService) {
    // translate.addLangs(['fr-fr']); will come soon
    translate.setTranslation('en-uk', defaultLanguage);
    translate.setDefaultLang('en-uk');
    /* french translation will come soon*/
    translate.use('en-uk');
  } 
}
