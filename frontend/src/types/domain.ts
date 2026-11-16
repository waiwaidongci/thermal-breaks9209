export type User={id:number;email:string;name:string;role:string};
export type Batch={id:number;name:string;filename:string;description:string};
export type Point={id:number;batch_id:number;sequence:number;recorded_at:string;temperature:number};
export type Segment={id?:number;run_id?:number;position:number;start:number;end:number;mean:number;rss:number};
export type Run={id:number;batch_id:number;name:string;status:string;config:any;result:any;error?:string;created_at:string};
export type Note={id:number;run_id:number;name:string;segment_ids:number[];segment_snapshot:Segment[];interpretation:string;next_step:string;status:string;review_note:string;created_by:string};
