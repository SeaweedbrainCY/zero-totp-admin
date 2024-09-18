import { Component, OnInit } from '@angular/core';
import { faUsers, faUserLock, faEye, faTrash, faXmark,faCircleNotch, faLockOpen, faHand, faChevronRight, faChevronDown } from '@fortawesome/free-solid-svg-icons';
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
  faChevronDown=faChevronDown;
  faChevronRight=faChevronRight;
  faLockOpen = faLockOpen;
  faHand = faHand;
  faCircleNotch = faCircleNotch;
  faXmark = faXmark;
  user_info_modal_id : string | undefined;
  users: any[] = [];
  confirm_disable_modal_active = false;
  disabling_user_id: string | undefined;
  is_disabling: boolean = false;
  confirm_delete_modal_active = false;
  deleting_user_id: string | undefined;
  loading = true;
  is_unblocking= false;
  is_deleting=false;
  deletion_timer = 5;
  interval:any=undefined;
  selected_row_user_id: number = -1;

 
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
    this.loading = true
    this.http.get("/api/v1/users/all",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        const body = JSON.parse(JSON.stringify(response.body));
        this.users = body.users;
      }
      this.loading = false;
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    } else {
      console.error(error);
      this.utils.toastError(this.toastr, "Impossible to get users", error.error.message)
    }
    this.loading = false;
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
    this.http.put("/api/v1/users/block/"+this.disabling_user_id, {}, {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 201) {
        this.get_all_users();
        this.is_disabling = false;
        this.utils.toastSuccess(this.toastr, "Operation success", "User #"+ this.disabling_user_id + " diabled")
        this.close_disable_modal();
      } else {
        this.is_disabling = false;
        this.utils.toastError(this.toastr, "The user might not be blocked ", "Got unexpected status code " + response.status) 
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

  unblock(user_id: string) {
    
    this.is_unblocking = true;
    this.http.put("/api/v1/users/unblock/"+user_id, {}, {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 201) {
        this.get_all_users();
        this.is_unblocking = false;
        this.utils.toastSuccess(this.toastr, "Operation success", "User #"+ user_id + " unblocked")
        this.close_disable_modal();
      } else {
        this.is_unblocking = false;
        this.utils.toastError(this.toastr, "The user might not be unblocked ", "Got unexpected status code " + response.status) 
        this.close_disable_modal();
      }
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    } else {
      console.error(error);
      this.utils.toastError(this.toastr, "Impossible to unblock user", error.error.message)
      this.close_disable_modal();
      this.is_unblocking = false;
    }
  });
  }

  confirm_delete_user(){
    this.is_deleting = true;
    this.http.delete("/api/v1/users/"+this.deleting_user_id, {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 201) {
        this.get_all_users();
        this.is_deleting = false;
        this.utils.toastSuccess(this.toastr, "Operation success", "User #"+ this.deleting_user_id + " permanently deleted")
        this.close_delete_modal();
      } else {
        this.is_deleting = false;
        this.utils.toastError(this.toastr, "The user might not be deleted ", "Got unexpected status code " + response.status) 
        this.close_delete_modal();
      }
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    } else if (error.status === 403) {
      this.utils.toastError(this.toastr, "Impossible to delete user",  error.error.error)
      this.close_delete_modal();
      this.is_deleting = false
    } else {
      this.utils.toastError(this.toastr, "Impossible to delete user", error.error.message)
      this.close_delete_modal();
      this.is_deleting = false;
    }
  });
  }

  close_delete_modal(){
    if(!this.is_deleting){
      this.confirm_delete_modal_active = false;
      this.deleting_user_id = undefined;
    }
  }

  delete_user(user_id: string) {
    this.confirm_delete_modal_active = true;
    this.deleting_user_id = user_id;
    this.deletion_timer = 5;
    this.start_interval();
  }

  start_interval() {
   this.interval = setInterval(() => {
      this.deletion_timer -= 1;
      if(this.deletion_timer <= 0) {
        this.stop_interval();
      }
    }, 1000);
  }

  stop_interval() {
    if(this.interval != undefined){
      clearInterval(this.interval);
    }
  }

  select_row(user_id: number) {
    if(this.selected_row_user_id === user_id) {
      this.selected_row_user_id = -1;
    } else {
      this.selected_row_user_id = user_id;
    }
  }

  boolean_to_string(value: boolean) {
    return value ? "Enabled" : "Disabled";
  }



  
}
