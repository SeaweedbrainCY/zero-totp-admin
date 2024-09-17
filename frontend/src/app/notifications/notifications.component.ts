import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { faBell, faCheckToSlot, faUserCheck, faCircleNotch, faTrashCan, faXmark } from '@fortawesome/free-solid-svg-icons';
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
  faXmark=faXmark;
  faTrashCan=faTrashCan;
  notif_enabled: boolean = false;
  notif_auth_user_only: boolean = false;
  notifications: notification_data[]=[];
  notifMessage= "";
  localTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  displayed_notification: notification_data | undefined;
  notifcation_id_to_display: string | undefined;
  zero_totp_displayed_notification_id: string | undefined;
  will_the_current_notification_be_displayed: boolean = false;
  confirm_delete_modal_active=false;
  notification_id_to_delete: string | undefined;
  is_deleting: boolean = false;


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
            this.getAllNotifcations();
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
        this.notifications = this.notifications!.sort((a, b) => (a.timestamp > b.timestamp) ? -1 : 1);
        if (this.notifcation_id_to_display != undefined){
          this.displayNotification();
        }
        this.defineNotificationToDisplayInZeroTOTP();
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
    if (this.displayed_notification == undefined){
      this.utils.toastError(this.toastr, "Notification not found", "")
      this.router.navigate(['/notifications']);
      return;
    } else {
      this.notifMessage = this.displayed_notification!.message;
      this.notif_enabled = this.displayed_notification!.enabled;
      this.notif_auth_user_only = this.displayed_notification!.auth_user_only;
      this.notifExpiration = this.displayed_notification!.expiration_timestamp == null ? undefined : this.timestampToLocaleDate(this.displayed_notification!.expiration_timestamp);
    }
    
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
      if(this.notifcation_id_to_display == undefined){
          this.http.post("/api/v1/notification" , body, {withCredentials:true, observe: 'response'}).subscribe((response) => {
            if (response.status === 201) {
              const body = JSON.parse(JSON.stringify(response.body));
              this.translate.get("notifications.create.success").subscribe((translation)=>{
                this.utils.toastSuccess(this.toastr, translation, "")
              });
              this.router.navigate(['/notifications/' + body.id]);
            } else {
              this.translate.get("notifications.errors.save").subscribe((translation)=>{
                this.utils.toastSuccess(this.toastr, translation, "")
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
        } else {
          this.http.put("/api/v1/notification/"+this.notifcation_id_to_display , body, {withCredentials:true, observe: 'response'}).subscribe((response) => {
            if (response.status === 201) {
              this.translate.get("notifications.update.success").subscribe((translation)=>{
                this.utils.toastSuccess(this.toastr, translation, "")
              });
              this.getAllNotifcations();
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
  }

  get_notification_by_id(uuid:string|undefined){
    if(uuid == undefined){
      return {id: 'error', message: "If you see this, an error occurred. You should try again and not try to delete.", timestamp: Number(new Date().getTime() / 1000), expiration_timestamp: null, auth_user_only: false, enabled: false}
    }
    return this.notifications!.find((element) => element.id == uuid);
  }

  public defineNotificationToDisplayInZeroTOTP(){
    console.log("defineNotificationToDisplayToUsers");
    let enabled_notif: notification_data[] = this.notifications!.filter((element) => element.enabled)
    if( this.notifMessage != "" && this.notif_enabled){
      const current_notif : notification_data = {
        id: 'new',
        message: this.notifMessage,
        timestamp: Number(new Date().getTime() / 1000),
        expiration_timestamp: this.notifExpiration == undefined ? null : Number(new Date(this.notifExpiration).getTime() / 1000),
        auth_user_only: this.notif_auth_user_only,
        enabled: this.notif_enabled
      }
      enabled_notif.push(current_notif);
    }
    enabled_notif = enabled_notif.sort((a, b) => (a.timestamp > b.timestamp) ? -1 : 1);
    console.log(enabled_notif);
    this.will_the_current_notification_be_displayed = false;
    for (let notif of enabled_notif){
      if(notif.expiration_timestamp == null || notif.expiration_timestamp > Number(new Date().getTime() / 1000)){
        if(notif.id == 'new'){
          this.will_the_current_notification_be_displayed = true;
        } else {
          this.zero_totp_displayed_notification_id = notif.id;
          console.log("notification_id_displayed_to_users: " + this.zero_totp_displayed_notification_id);
          return;
        }
      }
    }
    console.log("notification_id_displayed_to_users: undefined");
    this.zero_totp_displayed_notification_id = undefined;
  }
  
  private hasNotificationBennModified(){
    return (this.notifcation_id_to_display == undefined && this.notifMessage != "") || this.notifcation_id_to_display != undefined && ( this.notifMessage != this.displayed_notification?.message || this.notif_enabled != this.displayed_notification?.enabled || this.notif_auth_user_only != this.displayed_notification?.auth_user_only || !(this.notifExpiration == undefined && this.displayed_notification?.expiration_timestamp == null) || ((this.notifExpiration != undefined || this.displayed_notification?.expiration_timestamp != null) && this.displayed_notification!.expiration_timestamp != Number(new Date(this.notifExpiration!).getTime() / 1000)))
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

  public confirm_delete(){
    this.is_deleting = true;
    this.http.delete("/api/v1/notification/"+this.notification_id_to_delete, {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        this.translate.get("notifications.delete.success").subscribe((translation)=>{
          this.utils.toastSuccess(this.toastr, translation, "")
        });
        this.close_delete_modal();
        this.router.navigate(['/notifications']);
      } else {
        this.translate.get("notifications.errors.delete").subscribe((translation)=>{
          this.utils.toastError(this.toastr, translation, "")
        });
        this.is_deleting = false;
      }
    }, (error) => {
      if(error.status === 401) {
        this.redirectToLogin();
      } else if (error.status === 400){
        this.utils.toastError(this.toastr, "Impossible to delete this notification", error.error.error)
      } else {
          console.error(error);
          this.utils.toastError(this.toastr, "Impossible to delete this notification", error.message)
      }
      this.is_deleting = false;
    });
   
  }

  public close_delete_modal(){
    if (this.is_deleting){
      return;
    }
    this.confirm_delete_modal_active = false;
    this.notification_id_to_delete = undefined;
  }

  public open_delete_modal(uuid:string){
    this.confirm_delete_modal_active = true;
    this.notification_id_to_delete = uuid;
  }
}


