import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './modules/app-routing/app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {TopNavModule} from "./modules/top-nav/top-nav.module";
import {HttpClientModule} from "@angular/common/http";
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { CorrelationsComponent } from './modules/correlations/components/correlations/correlations.component';
import {MatDividerModule} from "@angular/material/divider";

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    NgbModule,
    TopNavModule,
    HttpClientModule,
    FontAwesomeModule,
    MatDividerModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
