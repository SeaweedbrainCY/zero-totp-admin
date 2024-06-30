import { Component } from '@angular/core';
import { faUsers, faUserLock, faEye, faTrash } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrl: './users.component.scss'
})
export class UsersComponent {
  faUsers = faUsers;
  faUserLock = faUserLock;
  faEye = faEye;
  faTrash = faTrash;
  user_info_modal = true;

  constructor() { }
}
