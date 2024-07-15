import { Component } from '@angular/core';
import { faChartLine, faUsersRectangle, faServer, faCircleNotch } from '@fortawesome/free-solid-svg-icons';
import { NgChartsConfiguration } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from "chart.js";
import { HttpClient } from '@angular/common/http';
import { OnInit } from '@angular/core';
import {formatDate} from '@angular/common';

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
  public lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: [
      '01/01/2024',
      '01/02/2024',
      '01/03/2024',
      '01/04/2024',
      '01/05/2024',
      '01/06/2024',
      '01/07/2024'
    ],
    datasets: [
      {
        data: [ 3, 4, 5, 10, 20, 21, 22 ],
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


  constructor(
    private http: HttpClient

  ) { 
  }

  ngOnInit(): void {
   this.getStats();
  }


  private getStats() {
    this.http.get("/api/v1/stats/users",  {withCredentials:true, observe: 'response'}).subscribe((response) => {
      if (response.status === 200) {
        const body = JSON.parse(JSON.stringify(response.body));
        console.log(body)
        this.total_user = body.total_users;
        this.total_verified_user = body.verified_users;
        this.total_blocked_user = body.blocked_users;
        console.log(this.total_blocked_user)
      }
  }, (error) => {
    console.error(error);
  });
  }

  public sortByDate(array:Array<string>): void {
    array.sort((a,b) => {
        return Date.parse(a) - Date.parse(b) ;

    });
}

}
