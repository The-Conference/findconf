"use strict";(self.webpackChunkconference=self.webpackChunkconference||[]).push([[219,41],{7659:function(e,s,n){n.r(s),n.d(s,{default:function(){return T}});var c=n(4165),a=n(5861),r=n(9439),t=n(2791),l=n(7689),i=n(2838),d=n(9641),o=n(9434),f=n(691),h=n(8131),u=n(458),x=n(8703),j=n.n(x),_=n(1243),p=n(8414),v=n(6971),m=n(6549),g=n(7179);var b=n.p+"static/media/Divider2.39823dde5a270c9a5a3c49312c86e824.svg";var N=n.p+"static/media/tg.b0589b5e724dd92cc132ddb6a0e049d9.svg";var k=n.p+"static/media/wapp.7dc3f3267bee9b39fd8d08466208e48a.svg";var w=n.p+"static/media/email.ed2c0453346e3ec2c903c4568a727f97.svg";var C=n.p+"static/media/vk.506de7ed26dd081a426ce00488a79dc2.svg",Z=n(2987);var L=n.p+"static/media/share.ff759aa91556d3b557281356659bf86e.svg",S=n(184);function D(){var e=(0,t.useState)(!1),s=(0,r.Z)(e,2),n=s[0],c=s[1],a=(0,t.useRef)(null);(0,Z.Z)(a,(function(){return c(!1)}));var i=(0,l.TH)().pathname,d="test.theconf.ru".concat(i);return(0,S.jsxs)(S.Fragment,{children:[(0,S.jsx)("img",{className:"share",src:L,alt:"share",onClick:function(){return c(!n)}}),n&&(0,S.jsxs)("div",{className:"sharebutton",ref:a,children:[(0,S.jsxs)("div",{children:[(0,S.jsx)("h1",{children:"\u041f\u043e\u0434\u0435\u043b\u0438\u0442\u044c\u0441\u044f"}),(0,S.jsx)("svg",{onClick:function(){return c(!n)},width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,S.jsx)("path",{d:"M13.53 12.47C13.823 12.763 13.823 13.238 13.53 13.531C13.384 13.677 13.192 13.751 13 13.751C12.808 13.751 12.616 13.678 12.47 13.531L6.99999 8.061L1.52999 13.531C1.38399 13.677 1.19199 13.751 0.999993 13.751C0.807993 13.751 0.615994 13.678 0.469994 13.531C0.176994 13.238 0.176994 12.763 0.469994 12.47L5.94 7.00002L0.469994 1.53005C0.176994 1.23705 0.176994 0.762018 0.469994 0.469018C0.762994 0.176018 1.238 0.176018 1.531 0.469018L7.001 5.93905L12.471 0.469018C12.764 0.176018 13.239 0.176018 13.532 0.469018C13.825 0.762018 13.825 1.23705 13.532 1.53005L8.06199 7.00002L13.53 12.47Z",fill:"#00002E"})})]}),(0,S.jsx)("img",{src:b,alt:""}),(0,S.jsxs)("div",{className:"sharebutton-social",children:[(0,S.jsx)(p.Z,{url:d,children:(0,S.jsx)("img",{src:N,alt:"telegram"})}),(0,S.jsx)(v.Z,{url:d,children:(0,S.jsx)("img",{src:k,alt:"watsapp"})}),(0,S.jsx)(m.Z,{url:d,children:(0,S.jsx)("img",{src:w,alt:"email"})}),(0,S.jsx)(g.Z,{url:d,children:(0,S.jsx)("img",{src:C,alt:"vk"})})]})]})]})}var y=n(1235),T=function(){var e,s=(0,l.UO)().confId,n=(0,o.v9)((function(e){return e.conferences})),x=n.conferences,p=n.oneConference,v=n.isLoading,m=(0,o.I0)(),g=(0,t.useState)(!0),b=(0,r.Z)(g,2),N=b[0],k=b[1],w=(0,t.useState)(!1),C=(0,r.Z)(w,2),Z=C[0],L=C[1],T=p;(0,t.useEffect)((function(){var e=function(){var e=(0,a.Z)((0,c.Z)().mark((function e(){var n,a;return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(m((0,d.Av)()),n=localStorage.getItem("auth_token"),a={Authorization:"Token ".concat(n),Accept:"application/json"},e.prev=3,!n){e.next=9;break}return e.next=7,_.Z.get("https://test.theconf.ru/api/".concat(s,"/"),{headers:a}).then((function(e){return m((0,d.E4)(e.data))}));case 7:e.next=11;break;case 9:return e.next=11,_.Z.get("https://test.theconf.ru/api/".concat(s,"/")).then((function(e){return m((0,d.E4)(e.data))}));case 11:e.next=16;break;case 13:e.prev=13,e.t0=e.catch(3),m((0,d.xT)(e.t0.message));case 16:case"end":return e.stop()}}),e,null,[[3,13]])})));return function(){return e.apply(this,arguments)}}();e(),m((0,d.rR)()),window.scrollTo(0,0)}),[s,m]);return!T&&!v&&x.length>0&&(e=(0,S.jsx)(i.default,{})),v&&(e=(0,S.jsx)(f.ZP,{})),p&&(e=(0,S.jsxs)("div",{className:"full-conference__container",children:[(0,S.jsxs)("div",{className:"full-conference__container-top",children:[(0,S.jsx)("span",{className:"\u041e\u0436\u0438\u0434\u0430\u0435\u0442\u0441\u044f \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f"===T.conf_status||"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0441\u043a\u043e\u0440\u043e \u043d\u0430\u0447\u043d\u0451\u0442\u0441\u044f"===T.conf_status||"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u043d\u0430\u0447\u0430\u043b\u0430\u0441\u044c"===T.conf_status||"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0438\u0434\u0451\u0442"===T.conf_status||"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u043e\u043a\u043e\u043d\u0447\u0435\u043d\u0430"===T.conf_status?"yellow-status":"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u044f \u0437\u0430\u043f\u043b\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0430"===T.conf_status||"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u044f \u0441\u043a\u043e\u0440\u043e \u043d\u0430\u0447\u043d\u0451\u0442\u0441\u044f"===T.conf_status||"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u044f \u0438\u0434\u0451\u0442"===T.conf_status?"green-status":"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u044f \u043f\u0440\u0438\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u0430"===T.conf_status?"orange-status":"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u044f \u043e\u043a\u043e\u043d\u0447\u0435\u043d\u0430"===T.conf_status?"grey-status":"red-status",children:T.conf_status}),(0,S.jsxs)("div",{className:"social",children:[(0,S.jsx)(y.Z,{id:T.id,favorite:T.is_favorite,type:"full"}),(0,S.jsx)(D,{})]})]}),(0,S.jsxs)("div",{className:"full-conference__title",children:[(0,S.jsx)("h1",{children:T.conf_name}),(0,S.jsxs)("small",{children:["\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430 \u043d\u0430 ",T.conf_date_begin," "]})]}),(0,S.jsxs)("div",{className:"full-conference__card",children:[(0,S.jsxs)("div",{className:"full-conference__card-flex",children:[(0,S.jsxs)("div",{children:[(0,S.jsx)("span",{children:"\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f:"}),null===T.conf_date_end?new Date(T.conf_date_begin).toLocaleDateString("ru",h.Y).slice(0,-3):null===T.conf_date_begin?new Date(T.conf_date_end).toLocaleDateString("ru",h.Y).slice(0,-3):T.conf_date_end!==T.conf_date_begin?new Date(T.conf_date_begin).toLocaleDateString("ru",h.Y).slice(0,-3)+" - "+new Date(T.conf_date_end).toLocaleDateString("ru",h.Y).slice(0,-3):new Date(T.conf_date_begin).toLocaleDateString("ru",h.Y).slice(0,-3)]}),(0,S.jsxs)("div",{children:[(0,S.jsx)("span",{children:"\u0424\u043e\u0440\u043c\u0430 \u0443\u0447\u0430\u0441\u0442\u0438\u044f:"}),(0,S.jsx)("span",{className:"both",children:T.online?"\u043e\u043d\u043b\u0430\u0439\u043d":""}),(0,S.jsx)("span",{className:"both",children:T.offline?"\u043e\u0444\u0444\u043b\u0430\u0439\u043d":""})]}),(0,S.jsx)("div",{children:(0,S.jsx)("span",{children:"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f:"})}),(0,S.jsxs)("div",{children:[(0,S.jsx)("span",{children:"\u041f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u044f:"}),(0,S.jsxs)("span",{className:"online",children:[(0,S.jsx)("span",{className:"publish",children:T.rinc?"\u0420\u0418\u041d\u0426   ":""}),(0,S.jsx)("span",{className:"publish",children:T.vak?"\u0412\u0410\u041a   ":""}),(0,S.jsxs)("span",{className:"publish",children:[" ",T.wos?"WOS    ":""]}),(0,S.jsx)("span",{className:"publish",children:!T.scopus&&!T.wos&&!T.vak&&!T.rinc&&"\u0431\u0435\u0437 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438"}),(0,S.jsx)("span",{className:"publish",children:T.scopus?"Scopus    ":""})]})]})]}),(0,S.jsx)("hr",{}),(0,S.jsxs)("div",{className:"full-conference__card-block",children:[(0,S.jsxs)("div",{children:[(0,S.jsx)("span",{children:"\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0442\u043e\u0440:"})," ",T.un_name]}),(0,S.jsx)("hr",{}),(0,S.jsxs)("div",{children:[(0,S.jsx)("span",{children:"\u0422\u0435\u043c\u0430\u0442\u0438\u043a\u0430:"})," ",T.tags.map((function(e){return(0,S.jsxs)("span",{className:"online",children:[" ",e.name]})}))]})]})]}),(0,S.jsxs)("div",{className:"full-conference__tabs",children:[(0,S.jsx)("button",{className:N?"button-active":"button-passive",onClick:function(){!0===Z&&(L(!1),k(!0))},children:"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435"}),(0,S.jsx)("button",{className:Z?"button-active":"button-passive",onClick:function(){!0===N&&k(!1),L(!0)},children:"\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b"})]}),N&&!Z&&(0,S.jsxs)("div",{className:"full-conference__desc",children:[(0,S.jsx)("h1",{children:"\u0423\u0441\u043b\u043e\u0432\u0438\u044f \u0443\u0447\u0430\u0441\u0442\u0438\u044f"}),null!==T.conf_desc&&0===T.conf_desc.length&&(0,S.jsx)("a",{href:T.conf_card_href,rel:"noreferrer",target:"_blank",children:"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435 \u043e \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"})||null!==T.conf_card_href&&T.conf_card_href.length>0&&(0,S.jsxs)("pre",{children:[(0,S.jsx)("div",{className:"full-conference__desc-parsed",dangerouslySetInnerHTML:{__html:j().sanitize(T.conf_desc)}}),(0,S.jsx)("div",{children:(0,S.jsx)("a",{href:T.conf_card_href,rel:"noreferrer",target:"_blank",children:"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435 \u043e \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"})})]})]}),!N&&Z&&(0,S.jsx)("div",{className:"full-conference__contacts",children:(0,S.jsxs)("pre",{children:[(0,S.jsxs)("div",{children:[(0,S.jsx)("span",{children:"\u0410\u0434\u0440\u0435\u0441 "}),(0,S.jsx)("br",{})," ",(0,S.jsx)("p",{children:T.conf_address})]}),(0,S.jsxs)("div",{children:[(0,S.jsx)("span",{children:"\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f "}),(0,S.jsx)("br",{})," ",(0,S.jsx)("p",{children:T.contacts})]}),(0,S.jsxs)("div",{children:[(0,S.jsx)("p",{className:"useful-links",children:"\u041f\u043e\u043b\u0435\u0437\u043d\u044b\u0435 \u0441\u0441\u044b\u043b\u043a\u0438 "}),(0,S.jsx)("br",{}),T.conf_card_href&&(0,S.jsx)("a",{rel:"noreferrer",target:"_blank",href:T.conf_card_href,children:"\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a"}),(0,S.jsx)("br",{}),T.reg_href&&(0,S.jsx)("a",{rel:"noreferrer",target:"_blank",href:T.reg_href,children:"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f"})]})]})})]})),(0,S.jsxs)(S.Fragment,{children:[(0,S.jsx)("div",{className:"full-conference",children:e}),T&&(0,S.jsx)("div",{style:{paddingBottom:"30px"},children:(0,S.jsx)(u.default,{data:"prev4",keywords:T.themes,id:T.id})})]})}}}]);
//# sourceMappingURL=219.988bee04.chunk.js.map