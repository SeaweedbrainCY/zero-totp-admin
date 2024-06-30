import { Component } from '@angular/core';
import { faChartLine, faUsersRectangle, faServer } from '@fortawesome/free-solid-svg-icons';
import { NgChartsConfiguration } from 'ng2-charts';
import { ChartConfiguration, ChartOptions, ChartType } from "chart.js";

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent {
  faUsersRectangle=faUsersRectangle
  faChartLine = faChartLine;
  faServer=faServer;
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

  constructor() { }

}
