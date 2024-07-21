import { Component } from '@angular/core';
import { faChartLine, faUsersRectangle, faServer, faCircleNotch } from '@fortawesome/free-solid-svg-icons';
import { NgChartsConfiguration } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType, UpdateMode } from "chart.js";
import { HttpClient } from '@angular/common/http';
import { OnInit } from '@angular/core';
import { Utils } from '../common/Utils/utils.service';
import { ToastrService } from 'ngx-toastr';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {
  faUsersRectangle=faUsersRectangle
  faChartLine = faChartLine;
  faServer=faServer;
  faCircleNotch=faCircleNotch;
  total_user:number|undefined;
  total_verified_user:number|undefined;
  total_blocked_user:number|undefined;
  rate_limited_ip:number|undefined;
  rate_limited_emails:number|undefined;
  public lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: [ "01", "02"
    ],
    datasets: [
      {
        data: [10,10 ],
        label: 'Total users',
        fill: true,
        tension: 0.5,
        borderColor: 'rgb(90, 169, 230)',
        backgroundColor: 'rgba(90, 169, 230,.3)'
      }
    ]
  };
  public lineChartOptions: ChartOptions<'line'> = {
    responsive: false
  };
  public lineChartLegend = true;
  isCurrentlyRedirecting = false;


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
        this.getStats();
        this.getTimeChart();
        this.getRateLimitedStats();
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
          resolve(false);
      }
    });
    });
  }

  private getStats() {
    this.http.get("/api/v1/stats/users/category",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        const body = JSON.parse(JSON.stringify(response.body));
        console.log(body)
        this.total_user = body.total_users;
        this.total_verified_user = body.verified_users;
        this.total_blocked_user = body.blocked_users;
        console.log(this.total_blocked_user)
      }
     
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    } else {
      console.error(error);
      this.utils.toastError(this.toastr, "Impossible to get users stats", error.error.message)
    }
  });
  }

  private getTimeChart() {
    this.http.get("/api/v1/stats/users/timechart",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        
        const body = JSON.parse(JSON.stringify(response.body));
        const date_array = Object.keys(body)
        const labels= this.sortByDate(date_array)
        const data = labels.map((date) => {
          return body[date]
        });
        this.lineChartData = {
        labels: labels,
        datasets: [
          {
            data: data,
            label: 'Total users',
            fill: true,
            tension: 0.3,
            borderColor: 'rgb(90, 169, 230)',
            backgroundColor: 'rgba(90, 169, 230,.3)'
          }
        ]
      };

        
      }
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    }
    console.error(error);
    this.utils.toastError(this.toastr, "Impossible to get new users stats", error.error.message)

  });
  }

  public sortByDate(array:Array<string>): Array<string> {
    return array.sort((a,b) => {
        return Date.parse(a) - Date.parse(b) ;

    });
}

public getRateLimitedStats() {
  
  this.http.get("/api/v1/stats/server/rate-limiting",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
    if (response.status === 200) {
      const body = JSON.parse(JSON.stringify(response.body));
      console.log(body)
      this.rate_limited_ip = body.rate_limited_ip;
      this.rate_limited_emails = body.rate_limited_emails;
    } else {
      this.utils.toastError(this.toastr, "Failed to get rate limited stats", "")
    }
  }, (error) => {
    if(error.status === 401) {
      this.redirectToLogin();
      return;
    }
    console.error(error);
    this.utils.toastError(this.toastr, "Impossible to get rate limiting stats", error.error.message)
  });
}

private redirectToLogin() {

  this.utils.toastError(this.toastr, "You are not authenticated", "")
  this.router.navigate(['/login']);
  
}

}
