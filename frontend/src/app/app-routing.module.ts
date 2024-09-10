import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { OverviewComponent } from './overview/overview.component';
import { UsersComponent } from './users/users.component';
import { LogoutComponent } from './logout/logout.component';
import { NotificationsComponent } from './notifications/notifications.component';

export const routes: Routes = [
  {path:'login', component: LoginComponent},
  {path:"logout", component: LogoutComponent},
  {path:"overview", component: OverviewComponent},
  {path:"users", component: UsersComponent},
  {path:"notifications", component: NotificationsComponent},
  {path:"notifications/:id", component: NotificationsComponent},
  {path:'', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
