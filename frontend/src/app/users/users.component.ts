import { Component, OnInit } from '@angular/core';
import { faUsers, faUserLock, faEye, faTrash } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { Utils } from '../common/Utils/utils.service';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';
@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrl: './users.component.scss'
})
export class UsersComponent implements OnInit{
  faUsers = faUsers;
  faUserLock = faUserLock;
  faEye = faEye;
  faTrash = faTrash;
  user_info_modal = false;
  users: any[] = [];

 
  constructor(
    private http: HttpClient,
    private utils: Utils,
    private toastr: ToastrService,
    private router:Router
  ) { 
    
  }

  ngOnInit(): void {
    this.verifyAuthentication().then((isAuthenticated) => {
      if(isAuthenticated) {
        this.get_all_users();
      }
    });
  }

  private verifyAuthentication(): Promise<boolean> {
    return new Promise((resolve, reject) => {
      this.http.get("/api/v1/whoami",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
        if (response.status === 200) {
          resolve(true);
        }
    }, (error) => {
      if(error.status === 401) {
        this.redirectToLogin();
        resolve(false);
      } else {
          console.error(error);
          this.utils.toastError(this.toastr, "Impossible to verify authentication", error.error.message)
          this.redirectToLogin();
          resolve(false);
      }
    });
    });
  }

  private redirectToLogin() {

    this.utils.toastError(this.toastr, "You are not authenticated", "")
    this.router.navigate(['/login']);
    
  }

  private get_all_users() {
    this.http.get("/api/v1/users/all",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        const body = JSON.parse(JSON.stringify(response.body));
        console.log(body.users)
        this.users = body.users;
      }
     
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    } else {
      console.error(error);
      this.utils.toastError(this.toastr, "Impossible to get users", error.error.message)
    }
  });
  }
}
