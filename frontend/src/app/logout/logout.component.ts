import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { Utils } from '../common/Utils/utils.service';
import { Router, ActivatedRoute } from '@angular/router';
import {faCircleNotch} from '@fortawesome/free-solid-svg-icons';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrl: './logout.component.scss'
})
export class LogoutComponent implements OnInit {
  faCircleNotch=faCircleNotch;

  constructor(
    private http: HttpClient,
    private utils: Utils,
    private toastr: ToastrService,
    private router:Router,
    private translate: TranslateService,
  ) { }

  ngOnInit() {
    
    this.http.post("/api/v1/logout", {}, {withCredentials: true, observe: 'response'}).subscribe((response) => {
      this.translate.get("logout_component.success").subscribe((translation) => {
        this.utils.toastSuccess(this.toastr,translation, "");
        this.router.navigate(['/login']);
      });
    }, (error) => {
      if (error.status != 401) {
        this.translate.get("logout_component.error").subscribe((translation) => {
        this.utils.toastError(this.toastr, translation, "");
        });
      } else {
        this.translate.get("logout_component.success").subscribe((translation) => {
          this.utils.toastSuccess(this.toastr,translation, "");
          this.router.navigate(['/login']);
        });
      }
    });
  }

}
