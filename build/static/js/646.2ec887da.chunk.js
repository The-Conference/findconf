"use strict";(self.webpackChunkconference=self.webpackChunkconference||[]).push([[646],{7646:function(e,n,r){r.r(n),r.d(n,{default:function(){return k}});var t=r(3433),i=r(9439),c=r(2791),s=r(1087),a=r(7689);var l=r.p+"static/media/follow.b4f2d12bdf350dc85af593be3d7c024a.svg";var o=r.p+"static/media/following.01779a43ccf7f44a7f520d4b96eb6ce0.svg",d=r(9434),f=r(3105),p=r(9916),u=r(4757);var h=r.p+"static/media/whitecross.61344037d52ae9697008c0cc5b66151f.svg";var v=r.p+"static/media/greycross.361cfc398f7bb4f00f1d5ff1cc414c78.svg",x=r(184),m=function(){var e=(0,d.I0)(),n=(0,d.v9)(u.nt),r=(0,c.useState)(!1),t=(0,i.Z)(r,2),s=t[0],a=t[1];return(0,x.jsxs)(x.Fragment,{children:[(0,x.jsxs)("div",{className:"filter",children:[n.some((function(e){return!0===e.applied}))&&(0,x.jsx)("button",{className:n.some((function(e){return!0===e.applied}))?"filter__delete-button applied-hover":"filter__delete-button nonapplied-hover",onClick:function(){e((0,u.sn)()),e((0,p.fS)()),e((0,p.N0)())},children:n.some((function(e){return!0===e.applied}))&&(0,x.jsx)("img",{src:h,alt:"\u0443\u0434\u0430\u043b\u0438\u0442\u044c \u0444\u0438\u043b\u044c\u0442\u0440\u044b",width:"14",height:"14"})||(0,x.jsx)("img",{src:v,alt:"\u0443\u0434\u0430\u043b\u0438\u0442\u044c \u0444\u0438\u043b\u044c\u0442\u0440\u044b",width:"14",height:"14"})}),n.map((function(n){return(0,x.jsx)("div",{className:"filter__container",children:(0,x.jsx)("div",{onClick:function(){e((0,u.B1)(n.id)),e((0,p.YL)(n.name)),e((0,p.N0)())},className:!0===n.applied?"filter__container-button applied-hover":"filter__container-button nonapplied-hover",children:(0,x.jsx)("div",{children:n.name})},n.id)},n.id)}))]}),(0,x.jsxs)("div",{className:"filter-adaptive",children:[n.some((function(e){return!0===e.applied}))&&(0,x.jsx)("button",{style:{backgroundColor:n.some((function(e){return!0===e.applied}))?"#2c60e7":"#0000381A"},className:"filter-adaptive__delete-button",onClick:function(){e((0,u.sn)()),e((0,p.fS)()),e((0,p.N0)()),a(!1)},children:n.some((function(e){return!0===e.applied}))&&(0,x.jsx)("img",{src:h,alt:""})||(0,x.jsx)("img",{src:v,alt:""})}),(0,x.jsxs)("div",{className:"filter-adaptive__container-button",children:[(0,x.jsx)("span",{onClick:function(){return a(!s)},className:n.some((function(e){return!0===e.applied}))?"filter__delete-button applied-hover":"filter__delete-button nonapplied-hover",children:"\u0424\u0438\u043b\u044c\u0442\u0440\u044b"}),(0,x.jsx)("ul",{children:s&&n.map((function(n){return(0,x.jsx)("li",{className:!0===n.applied?"applied-hover":"nonapplied-hover",onClick:function(){e((0,u.B1)(n.id)),e((0,p.YL)(n.name)),e((0,p.N0)()),a(!s)},children:(0,x.jsx)("div",{children:n.name})},n.id)}))})]})]})]})},j=r(8131),g=r(7664),_=r(183),b=(r(3587),function(){return(0,x.jsxs)("div",{className:"empty",children:[(0,x.jsx)("img",{src:_.Z,alt:"\u043f\u0443\u0441\u0442\u043e",width:"450",height:"350"}),(0,x.jsx)("p",{children:"\u041d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e \u043d\u0438 \u043e\u0434\u043d\u043e\u0439 \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"})]})}),w=function(e,n){var r=new Date(e.getTime());r.setDate(r.getDate()+1);for(var t=[e,n];r<n;)t.push(new Date(r)),r.setDate(r.getDate()+1);return t.map((function(e){return e.toLocaleDateString()}))},N=function(e){e.paginate;var n=e.totalConferences,r=e.currentConference,t=e.addMore,i=(0,d.I0)();return(0,x.jsx)(x.Fragment,{children:r.length!==n&&(0,x.jsx)("div",{className:"showmore",onClick:function(){return i(t(10))},children:"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0435\u0449\u0435"})})},k=function(e){var n=e.data,r=e.keywords,u=e.id,h=(0,d.v9)((function(e){return e.conferences})),v=h.conferences,_=h.isLoading,k=h.currentPage,C=h.conferencesPerPage,D=(0,s.lr)(),L=(0,i.Z)(D,1)[0],S=(0,d.I0)(),y=(0,a.UO)(),U=y.periods,Y=y.date,O=JSON.parse(window.localStorage.getItem("fave"))||[],Z=(0,c.useState)(O),E=(0,i.Z)(Z,2),I=E[0],P=E[1],R=[],B=[],F=[],M=[],q=[],A=[],J=[];if("prev4"===n){var T=r.trim().split(" ").filter((function(e){return e.length>2})).join("|"),V=new RegExp(T,"gi");J=v.filter((function(e){return V.test(e.conf_name)||V.test(e.themes)}))}if("search-results"===n){var z=(q=L.get("q")).trim().split(" ").filter((function(e){return e.length>2})).join("|"),G=new RegExp(z,"gi");B=v.filter((function(e){return G.test(e.org_name)||G.test(e.conf_name)||G.test(e.themes)}))}if("date"===n){var H=v.map((function(e){var n=new Date(e.conf_date_begin),r=new Date(e.conf_date_end),t=e.id;return{per:w(n,r),ind:t}})),K=H.filter((function(e){return e.per.includes(Y)}));F=K.map((function(e){return e.ind}))}"periods"===n&&(A=U.split(",").map((function(e){return new Date(e)})),M=w(A[0],A[1]));var Q={all:v,favourites:v.filter((function(e){return!0===e.follow})),searchRes:B,date:v.filter((function(e){return F.includes(e.id)})),collection1:v.filter((function(e){return-1!==e.themes.toLowerCase().indexOf("\u0438\u0441\u0442\u043e\u0440\u0438\u044f".toLowerCase())})),collection2:v.filter((function(e){return-1!==e.themes.toLowerCase().indexOf("\u0444\u0438\u043b\u043e\u043b\u043e\u0433\u0438\u044f".toLowerCase())})),periods:v.filter((function(e){return M.includes(new Date(e.conf_date_begin).toLocaleDateString())||M.includes(new Date(e.conf_date_end).toLocaleDateString())})),prev1:v.filter((function(e){return-1!==e.themes.toLowerCase().indexOf("\u0438\u0441\u0442\u043e\u0440\u0438\u044f".toLowerCase())})).slice(0,2),prev2:v.filter((function(e){return-1!==e.themes.toLowerCase().indexOf("\u0444\u0438\u043b\u043e\u043b\u043e\u0433\u0438\u044f".toLowerCase())})).slice(0,2),prev3:v.slice(0,2),prev4:J.filter((function(e){return e.id!==u})).slice(0,2)};"all"===n&&(R=Q.all),"favourites"===n&&(R=Q.favourites),"search-results"===n&&(R=Q.searchRes),"collection1"===n&&(R=Q.collection1),"collection2"===n&&(R=Q.collection2),"date"===n&&(R=Q.date),"periods"===n&&(R=Q.periods),"prev1"===n&&(R=Q.prev1),"prev2"===n&&(R=Q.prev2),"prev3"===n&&(R=Q.prev3),"prev4"===n&&(R=Q.prev4);var W=k*C,X=W-C,$=R.slice(X,W);return(0,c.useEffect)((function(){S((0,p.c3)(I))}),[S,I]),(0,c.useEffect)((function(){"prev1"!==n&&"prev2"!==n&&"prev3"!==n&&"prev4"!==n&&S((0,p.N0)())}),[S,n]),(0,x.jsxs)("section",{className:"prev1"===n||"prev2"===n||"prev3"===n||"prev4"===n?"conference prev preview-bottom":"conference",children:[(0,x.jsxs)("div",{className:"conference__type",children:["all"===n&&(0,x.jsx)("div",{className:"back",children:(0,x.jsxs)(s.rU,{to:"/",children:[(0,x.jsx)("span",{className:"backarrow",children:"<"})," ",(0,x.jsx)("p",{children:"\u0412\u0441\u0435 \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"})]})}),"favourites"===n&&(0,x.jsx)("div",{className:"back",children:(0,x.jsxs)(s.rU,{to:"/",children:[(0,x.jsx)("span",{className:"backarrow",children:"<"})," ",(0,x.jsx)("p",{children:"\u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435"})]})}),"search-results"===n&&(0,x.jsxs)("div",{className:"back",children:[(0,x.jsx)("span",{className:"backarrow",children:"<"})," ",(0,x.jsxs)("p",{children:['\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u043e \u0437\u0430\u043f\u0440\u043e\u0441\u0443 "',q,'"']})]}),"collection1"===n&&(0,x.jsx)("div",{className:"back",children:(0,x.jsxs)(s.rU,{to:"/",children:[" ",(0,x.jsx)("span",{className:"backarrow",children:"<"})," ",(0,x.jsx)("p",{children:"\u0418\u0441\u0442\u043e\u0440\u0438\u044f"})]})}),"collection2"===n&&(0,x.jsx)("div",{className:"back",children:(0,x.jsxs)(s.rU,{to:"/",children:[(0,x.jsx)("span",{className:"backarrow",children:"<"})," ",(0,x.jsx)("p",{children:"\u0424\u0438\u043b\u043e\u043b\u043e\u0433\u0438\u044f"})]})}),"prev1"===n&&(0,x.jsxs)("a",{href:"/collection1",children:[(0,x.jsx)("p",{children:"\u0418\u0441\u0442\u043e\u0440\u0438\u044f"}),(0,x.jsx)("span",{children:">"})]}),"prev2"===n&&(0,x.jsxs)("a",{href:"/collection2",children:[(0,x.jsx)("p",{children:"\u0424\u0438\u043b\u043e\u043b\u043e\u0433\u0438\u044f"}),(0,x.jsx)("span",{children:">"})]}),"prev3"===n&&(0,x.jsxs)("a",{href:"/all",children:[(0,x.jsx)("p",{children:"\u0412\u0441\u0435 \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"}),(0,x.jsx)("span",{children:">"})]}),"prev4"===n&&R.length>0&&(0,x.jsxs)("div",{className:"similar",children:[(0,x.jsx)("p",{children:"\u041f\u043e\u0445\u043e\u0436\u0438\u0435 \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"}),(0,x.jsx)("span",{children:">"})]}),"date"===n&&(0,x.jsx)("div",{className:"back",children:(0,x.jsxs)(s.rU,{to:"/",children:[(0,x.jsx)("span",{className:"backarrow",children:"<"})," ",(0,x.jsx)("p",{children:"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438 \u043d\u0430 "}),(0,x.jsx)("span",{children:Y})]})}),"periods"===n&&(0,x.jsx)("div",{className:"back",children:(0,x.jsxs)(s.rU,{to:"/",children:[(0,x.jsx)("span",{className:"backarrow",children:"<"})," ",(0,x.jsx)("p",{children:"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"}),(0,x.jsxs)("span",{children:["c ",A[0].toLocaleDateString("ru",j.Y).slice(0,-7)]})," ",(0,x.jsxs)("span",{children:["\u043f\u043e ",A[1].toLocaleDateString("ru",j.Y).slice(0,-7)]})]})})]}),"prev1"!==n&&"prev2"!==n&&"prev3"!==n&&"prev4"!==n&&(0,x.jsx)(m,{}),_&&"prev1"!==n&&"prev2"!==n&&"prev3"!==n&&"prev4"!==n&&(0,x.jsx)(f.ZP,{})||_&&(0,x.jsx)(f.Lj,{}),!_&&0===R.length&&"favourites"!==n&&"prev1"!==n&&"prev2"!==n&&"prev3"!==n&&"prev4"!==n&&(0,x.jsx)(g.default,{}),!_&&0===R.length&&"favourites"===n&&(0,x.jsx)(b,{}),(0,x.jsx)("div",{className:"conference__container",children:!_&&R.length>0&&$.map((function(e){return(0,x.jsxs)("div",{className:"conference__block",children:[(0,x.jsxs)("div",{className:"conference__bg",children:[(0,x.jsxs)("div",{className:"conference__bg-top",children:[!1===e.register&&!1===e.finished&&(0,x.jsx)("span",{style:{backgroundColor:"#939393"},children:"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0437\u0430\u043a\u043e\u043d\u0447\u0435\u043d\u0430"})||!1===e.register&&!0===e.finished&&(0,x.jsx)("span",{style:{backgroundColor:"#939393"},children:"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u044f \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430"})||!0===e.register&&!1===e.finished&&(0,x.jsx)("span",{children:"\u0418\u0434\u0435\u0442 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f"}),(0,x.jsx)("img",{title:!1===e.follow?"\u0434\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432 \u0438\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435":"\u0443\u0434\u0430\u043b\u0438\u0442\u044c \u0438\u0437 \u0438\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0433\u043e",src:!1===e.follow?l:o,alt:"follow",onClick:function(){!function(e){I.includes(e)?P(I.filter((function(n){return n!==e}))):P([].concat((0,t.Z)(I),[e]))}(e.id),S((0,p.xe)(e.id))},width:"25",height:"24"})]}),(0,x.jsx)("div",{className:"conference__bg-middle",children:e.tags.map((function(e){return e.name})).length>0?(0,x.jsxs)("div",{children:["#",e.tags.map((function(e){return e.name}))]}):null}),(0,x.jsx)("div",{className:"conference__bg-bottom",children:null===e.conf_date_end&&null===e.conf_date_begin?"\u0434\u0430\u0442\u0430 \u0443\u0442\u043e\u0447\u043d\u044f\u0435\u0442\u0441\u044f":null!==e.conf_date_end?new Date(e.conf_date_begin).toLocaleDateString("ru",j.Y).slice(0,-3)+" - "+new Date(e.conf_date_end).toLocaleDateString("ru",j.Y).slice(0,-3):new Date(e.conf_date_begin).toLocaleDateString("ru",j.Y).slice(0,-3)}),(0,x.jsx)(s.rU,{"aria-label":"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435 \u043e \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438",style:{position:"absolute",bottom:"0",left:"0",right:"50px",top:"0"},to:"/conferences/".concat(e.id)}),(0,x.jsx)(s.rU,{"aria-label":"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435 \u043e \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438",style:{position:"absolute",bottom:"0",left:"0",right:"0",top:"50px"},to:"/conferences/".concat(e.id)})]}),(0,x.jsxs)("div",{className:"conference__tags",children:[(0,x.jsx)("div",{children:e.themes.split(",").map((function(e,n){return(0,x.jsx)("small",{children:e},n)}))}),(0,x.jsx)(s.rU,{to:"/conferences/".concat(e.id),children:(0,x.jsx)("div",{className:"conference__title",children:e.conf_name})})]})]},e.id)}))}),"prev1"!==n&&"prev2"!==n&&"prev3"!==n&&"prev4"!==n&&R.length>20&&(0,x.jsx)(N,{currentConference:$,totalConferences:R.length,paginate:p.V6,addMore:p.le})]})}},8131:function(e,n,r){r.d(n,{Y:function(){return t}});var t={year:"numeric",month:"long",day:"numeric"}}}]);
//# sourceMappingURL=646.2ec887da.chunk.js.map