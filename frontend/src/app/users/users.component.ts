import { Component, OnInit } from '@angular/core';
import { faUsers, faUserLock, faEye, faTrash, faXmark } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { Utils } from '../common/Utils/utils.service';
import { ToastrService } from 'ngx-toastr';
import { Router, ActivatedRoute } from '@angular/router';
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
  faXmark = faXmark;
  user_info_modal_id : string | undefined;
  users: any[] = [];
  confirm_disable_modal_active = false;
  disabling_user_id: string | undefined;
  is_disabling: boolean = false;
  confirm_delete_modal_active = false;
  deleting_user_id: string | undefined;

 
  constructor(
    private http: HttpClient,
    private utils: Utils,
    private toastr: ToastrService,
    private router:Router, 
    private route: ActivatedRoute
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

  disable_user(user_id: string) {
    this.confirm_disable_modal_active = true;
    this.disabling_user_id = user_id;
  }

  get_email_by_id(user_id: string | undefined) {
    if(user_id === undefined) {
      return "";
    }
    const user = this.users.find((user) => user.id === user_id);
    return user.email;
  }

  close_disable_modal() {
    if(!this.is_disabling){
      this.confirm_disable_modal_active = false;
    this.disabling_user_id = undefined;
    }
    
  }

  confirm_disable_user() {
    this.is_disabling = true;
    this.http.put("/api/v1/users/block", {user_id: this.disabling_user_id}, {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        this.get_all_users();
        this.is_disabling = false;
        this.utils.toastSuccess(this.toastr, "User disabled", "User "+ this.disabling_user_id + " diabled")
        this.close_disable_modal();
      }
     
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    } else {
      console.error(error);
      this.utils.toastError(this.toastr, "Impossible to disable user", error.error.message)
      this.close_disable_modal();
      this.is_disabling = false;
    }
  });
  }
}
