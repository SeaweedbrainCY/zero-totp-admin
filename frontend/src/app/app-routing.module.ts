import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { OverviewComponent } from './overview/overview.component';
import { UsersComponent } from './users/users.component';
import { LogoutComponent } from './logout/logout.component';

const routes: Routes = [
  {path:'login', component: LoginComponent},
  {path:"logout", component: LogoutComponent},
  {path:"overview", component: OverviewComponent},
  {path:"users", component: UsersComponent},
  {path:'', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
