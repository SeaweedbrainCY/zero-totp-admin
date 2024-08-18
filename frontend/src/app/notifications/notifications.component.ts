import { Component, OnInit } from '@angular/core';
import { faBell, faCheckToSlot, faUserCheck } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { Utils } from '../common/Utils/utils.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';


@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrl: './notifications.component.scss'
})
export class NotificationsComponent implements OnInit {
  faBell=faBell;
  expiration: string | undefined;
  faCheckToSlot=faCheckToSlot;
  faUserCheck=faUserCheck;
  notif_enabled: boolean = false;
  notif_auth_user_only: boolean = false;
  edit_notif_uuid: string | undefined;

  constructor(
    private http: HttpClient,
    private utils: Utils,
    private router:Router,
    private toastr: ToastrService,
    
  ) { }
  
  
  ngOnInit(): void {
    this.verifyAuthentication().then((isAuthenticated) => {
      if(isAuthenticated) {
        console.log("Authenticated");
      }});
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

  public selectNotification(uuid:string){
    
  }

  public saveNotificationConfig(){
    
  }

  public isNotificationDisplayed(uuid:string){
    return false;
  }
}
