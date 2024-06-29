import { Component } from '@angular/core';
import { faChartLine } from '@fortawesome/free-solid-svg-icons';


@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent {

  faChartLine = faChartLine;

  constructor() { }

}
