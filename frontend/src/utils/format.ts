export const number=(v:number,d=3)=>Number.isFinite(v)?v.toLocaleString('zh-CN',{maximumFractionDigits:d}):'—';export const date=(v:string)=>new Date(v).toLocaleString('zh-CN',{hour12:false});
