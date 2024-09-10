import { Component, OnInit } from '@angular/core';
import { faBell, faCheckToSlot, faUserCheck, faCircleNotch } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { Utils } from '../common/Utils/utils.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { TranslateService } from '@ngx-translate/core';


interface notification_body {
  message:string,
  expiration_timestamp_utc?:number,
  auth_user_only?:boolean,
  enabled?:boolean
}

interface notification_data {
    id: string,
    message: string,
    timestamp: number,
    expiration_timestamp: number | null,
    auth_user_only: boolean,
    enabled: boolean
  }

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrl: './notifications.component.scss'
})
export class NotificationsComponent implements OnInit {
  faBell=faBell;
  notifExpiration: string | undefined;
  faCheckToSlot=faCheckToSlot;
  faCircleNotch=faCircleNotch;
  faUserCheck=faUserCheck;
  notif_enabled: boolean = false;
  notif_auth_user_only: boolean = false;
  notifications: notification_data[] | undefined;
  notifMessage= "";
  localTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  displayed_notification: notification_data | undefined;
  notifcation_id_to_display: string | undefined;


  constructor(
    private http: HttpClient,
    private utils: Utils,
    private router:Router,
    private toastr: ToastrService,
    private translate: TranslateService, 
    private route: ActivatedRoute
    
  ) { 
    
  }

  
  
  
  ngOnInit(): void {
    
    this.verifyAuthentication().then((isAuthenticated) => {
      if(isAuthenticated) {
        this.route.params.subscribe(params => {
          if(params['id'] != undefined){
            this.notifcation_id_to_display = params['id']; 
            console.log("Displaying notification with id: " + this.notifcation_id_to_display);
            if(this.notifications != undefined){
              this.displayNotification();
          }
        } else {
          this.displayed_notification = undefined;
          this.notifcation_id_to_display = undefined;
        }
        window.scroll({ 
          top: 0, 
          left: 0, 
          behavior: 'smooth' 
      });
       });
        this.getAllNotifcations();
      }});
  }

  private getAllNotifcations(){
    this.http.get("/api/v1/notifications/all",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        const body = JSON.parse(JSON.stringify(response.body));
        this.notifications = body.notifications;
        if (this.notifcation_id_to_display != undefined){
          this.displayNotification();
        }
      }
  }, (error) => {
    if(error.status != 404) {
        console.error(error);
        this.utils.toastError(this.toastr, "Impossible to retrieve authentications. ", error.message)
    }
  });
  }

  displayNotification(){
    this.displayed_notification = this.notifications!.find((element) => element.id == this.notifcation_id_to_display);
    this.notifMessage = this.displayed_notification!.message;
    this.notif_enabled = this.displayed_notification!.enabled;
    this.notif_auth_user_only = this.displayed_notification!.auth_user_only;
    this.isNotificationDisplayed(this.notifcation_id_to_display!);
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
          this.utils.toastError(this.toastr, "Impossible to verify authentication", error.message)
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

  public saveNotificationConfig(){
    if(this.notifMessage == ""){
      this.translate.get("notifications.errors.empty").subscribe((translation)=>{
        this.utils.toastError(this.toastr, translation, "")
        return;
      });
    } else {
      let body: notification_body = {
        "message": this.notifMessage,
        "auth_user_only": this.notif_auth_user_only,
        "enabled": this.notif_enabled
      }
      if(this.notifExpiration != undefined && this.notifExpiration != "" && this.notifExpiration != null){
        const expiration_utc = new Date(this.notifExpiration).getTime();
        const unix_timestamp = expiration_utc / 1000;
        body["expiration_timestamp_utc"] = unix_timestamp;
      }
      this.http.post("/api/v1/notification", body, {withCredentials:true, observe: 'response'}).subscribe((response) => {
        if (response.status === 201) {
          const body = JSON.parse(JSON.stringify(response.body));
          this.router.navigate(['/notifications/' + body.id]);
        } else {
          this.translate.get("notifications.errors.save").subscribe((translation)=>{
            this.utils.toastError(this.toastr, translation, "")
          });
        }
      }, (error) => {
        if(error.status === 401) {
          this.redirectToLogin();
        } else if (error.status === 400){
          this.utils.toastError(this.toastr, "Impossible to save this user", error.error.error)
        } else {
            console.error(error);
            this.utils.toastError(this.toastr, "Impossible to save this user", error.message)
        }
      });
    }
  }

  public isNotificationDisplayed(uuid:string){
    return false;
  }
  
  private hasNotificationBennModified(){
    return this.notifcation_id_to_display != undefined && ( this.notifMessage != this.displayed_notification?.message || this.notif_enabled != this.displayed_notification?.enabled || this.notif_auth_user_only != this.displayed_notification?.auth_user_only || !(this.notifExpiration == undefined && this.displayed_notification?.expiration_timestamp == null) || ((this.notifExpiration != undefined || this.displayed_notification?.expiration_timestamp != null) && this.displayed_notification!.expiration_timestamp != Number(new Date(this.notifExpiration!).getTime() / 1000)))
  }

  public cancelNotification(){
    if(this.hasNotificationBennModified()){
      this.translate.get("notifications.confirm.cancel").subscribe((translation)=>{
        if(confirm(translation)){
          this.router.navigate(['/notifications']);
        }
      });
    } else {
      this.router.navigate(['/notifications']);
    }
  }

  public selectNotification(uuid:string){
    if(this.hasNotificationBennModified()){
      this.translate.get("notifications.confirm.cancel").subscribe((translation)=>{
        if(confirm(translation)){
          this.router.navigate(['/notifications/' + uuid]);
        }
      });
    } else {
      this.router.navigate(['/notifications/' + uuid]);
    }
  }

  public timestampToLocaleDate(timestamp:number){
    return new Date(timestamp * 1000).toLocaleString() + " (" + this.localTimezone + ")";
  }

  public isNotifSelected(uuid:string){
    return this.displayed_notification != undefined && this.displayed_notification.id == uuid;
  }
}
