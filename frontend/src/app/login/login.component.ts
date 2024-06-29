import { Component,OnInit } from '@angular/core';
import { faUser, faLock,  faCheck, faXmark, faFlagCheckered, faCloudArrowUp, faBriefcaseMedical, faEye, faEyeSlash, faKey, faSuitcaseMedical, faShieldHalved, faChevronDown, faChevronUp } from '@fortawesome/free-solid-svg-icons';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiService } from '../common/api-service/api-service.service';
import { Utils } from '../common/Utils/utils.service';

import { ToastrService } from 'ngx-toastr';
import { TranslateService } from '@ngx-translate/core';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  faUser=faUser;
  faLock=faLock;
  faCheck=faCheck;
  faXmark=faXmark;
  faSuitcaseMedical=faSuitcaseMedical;
  faShieldHalved=faShieldHalved;
  faKey=faKey;
  faChevronDown=faChevronDown;
  faChevronUp=faChevronUp;
  faFlagCheckered=faFlagCheckered;
  faCloudArrowUp=faCloudArrowUp;
  faEye=faEye;
  faEyeSlash=faEyeSlash;
  username:string = "";
  faBriefcaseMedical=faBriefcaseMedical;
  password:string = "";
  hashedPassword:string = "";
  isLoading = false;
  warning_message="";
  warning_message_color="is-warning";
  error_param: string|null=null;
  isPassphraseVisible=false;
  reset_admin_passphrase_modal=false;
  remember=false;
  reset_root_doc_displayed=false;
  reset_root_pass_displayed=false;

  constructor(
     private http: HttpClient,
    private router: Router,
    private route: ActivatedRoute,
    private translate: TranslateService,
    private toastr: ToastrService,
    private utils: Utils,
    ) {
    }


    ngOnInit(){
      console.log("init")
      
    }

  


  
  login(){
    if(this.username == "" || this.password == ""){
      this.translate.get("login.errors.empty").subscribe((translation)=>{
        this.utils.toastError(this.toastr,translation,"");
     });
      return;
    }
    this.isLoading = true;
    this.postLoginRequest()
    
  }

  



  postLoginRequest(){
    const data = {
      username: this.username,
      password: this.password
    }
    this.http.post(ApiService.API_URL+"/login",  data, {withCredentials: true, observe: 'response'}).subscribe((response) => {
      try{
        
      } catch(e){
        this.isLoading=false;
        console.log(e);
        this.translate.get("login.errors.server_error").subscribe((translation)=>{
        this.utils.toastError(this.toastr,translation,"")
      });
      }
      
    },
    (error) => {
      console.log(error);
      console.log(error.error.message)
      this.isLoading=false;
      if(error.status == 429){
        const ban_time = error.error.ban_time || "few";
        this.translate.get("login.errors.rate_limited",{time:String(ban_time)} ).subscribe((translation)=>{
        this.utils.toastError(this.toastr,translation,"")
      });
      } else if(error.error.message == "blocked"){
        this.translate.get("login.errors.account_blocked").subscribe((translation)=>{
        this.utils.toastError(this.toastr,translation,"")
      });
      } else {
        this.translate.get("generic_errors.error").subscribe((translation)=>{
          this.utils.toastError(this.toastr,translation + " : "+ this.translate.instant((error.error.message) ? error.error.message : ""),"")
        });
      }
      
    });
  }

 


 
}
