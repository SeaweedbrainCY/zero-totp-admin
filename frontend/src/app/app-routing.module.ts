import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { OverviewComponent } from './overview/overview.component';
import { UsersComponent } from './users/users.component';

const routes: Routes = [
  {path:'login', component: LoginComponent},
  {path:"overview", component: OverviewComponent},
  {path:"users", component: UsersComponent},
  {path:'', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
