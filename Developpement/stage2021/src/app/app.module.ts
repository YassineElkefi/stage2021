import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { FooterComponent } from './footer/footer.component';
import { AuthComponent } from './auth/auth.component';
import { InscriptionComponent } from './inscription/inscription.component';
import { AjoutClientComponent } from './ajout-client/ajout-client.component';
import { SupprClientComponent } from './suppr-client/suppr-client.component';
import { EnvoiDepotComponent } from './envoi-depot/envoi-depot.component';
import { ConsultComponent } from './consult/consult.component';
import { InterfaceAdminComponent } from './interface-admin/interface-admin.component';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    AuthComponent,
    InscriptionComponent,
    AjoutClientComponent,
    SupprClientComponent,
    EnvoiDepotComponent,
    ConsultComponent,
    InterfaceAdminComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
