%This code solves the Blasius laminar dynamic and thermal boundary
% layer problem numerically using the Euler numerical method. 
% The program solves the following equations:
% (1) Dynamic boundary layer equation: 2F'''+F.F''=0
% (2) Thermal boundary layer equation: 2T''+Pr.F.T'=0
% The code allows solving the velocity and temperature profiles of 
% the fluid flow along the flat plate for different fluids.
% By Dr.Abdelhamid BOUHELAL @18-03-2018
% https://www.abdelhamid-bouhelal.net/home
clear all;close all;clc;
global N dn bas Epsilon Eta
N=100000; dn=0.0001;
Eta=[0:N-1].*dn;
bas=1000;
Epsilon=1E-10;
iter=1;
hav=0.5;
hav2=1;
[f,g,h]=Euler(N,dn,hav);
[f,gav,h]=Euler(N,dn,hav2);
while (abs(1.0-g(N)) >= Epsilon) 
hnew=hav-(g(N)-1).*((hav-hav2)/(g(N)-gav(N)));
[f,g,h]=Euler(N,dn,hnew);
[f,gav,h]=Euler(N,dn,hav);
hav2=hav;
hav=hnew;
iter=iter+1;
Error=1.0-g(N);
disp([' h(1)= ',num2str(h(1))]);
hold on 
plot(iter,abs(g(N)-1),'-ro')
end
title('Convergence curve')
F=f;F1=g;F2=h;
figure
plot(Eta,F1,'LineWidth',02),hold on, plot(Eta,F2,'LineWidth',02)
legend('F', 'F'' ')
xlabel('\eta')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  [air,eau,ethanol, mercure];
pr=[0.7426, 7.0423, 17.1717, 0.0276];
%  pr=[0.1:0.1:5];
set(figure,'units','pixel','position',[400 200 450 350])
set(gca,'fontsize',12,'fontname','latex')
hold on
% Teta=Teta_trapz(F2,bas,N,Eta,pr);
 for j=1:length(pr)
 Teta=Teta_trapz(F2,bas,N,Eta,pr(j));
 plot(Eta(2:bas:N),Teta(2:bas:N),'-','LineWidth',02)
 end
grid on, box on
% xlabel('$\eta =y/ ( x*\nu / U_\infty)$' ,'interpreter','latex','FontSize',14)
xlabel('$\eta = \displaystyle\frac{y} { \sqrt{ \displaystyle\frac{x . \nu} {U_\infty} }}$ ','Interpreter','latex','FontSize',14)
ylabel('$ \theta = \displaystyle\frac{T-T_w}{T_\infty-T_w}$','interpreter','latex','FontSize',14)
legend('Air (Pr=0.7426)','Water (Pr=7.0423)','Ethanol (Pr= 17.1717)','Mercury (Pr= 0.0276)')
ylim([0 1])
fprintf('%6.5f \b \b  \b %6.5f \n',[Eta(2:bas:N);Teta(2:bas:N)])
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
co = [ 0 0    1.0000;
      0.8500    0.3250    0.0980;
      0.6350    0.0780    0.1840;
      0.4660    0.6740    0.1880;
      0.7500         0    0.7500;
    1.0000         0         0;
    0    0       0];
set(groot,'defaultAxesColorOrder',co)
set(figure,'units','pixel','position',[400 200 450 350])
set(gca,'fontsize',12,'fontname','latex')
U=[0.01,0.02,0.05,0.08,0.1,0.2];
% Eta=1:1:8;
%visc=0.0116*1E-6;
% visc=0.88*1E-6; %eau
% visc=15.6*1E-6; %air
% [air,eau,ethanol, Glycérol, mercure];
Pr=[0.7426, 7.0423, 17.1717, 0.0276]
 visc=[15*1E-6,  1E-6, 1.7E-6,  0.0116*1E-6];
del_t=[7, 3.1, 2.3, 28.1];
x=[0:0.01:10];
kk=4;
titre={'U_\infty = 0.01 m/s','U_\infty = 0.02 m/s','U_\infty = 0.05 m/s','U_\infty = 0.08 m/s','U_\infty = 0.1 m/s','U_\infty = 0.2 m/s'}
% titre=['U_\infty = 0.01 m/s','U_\infty = 0.02 m/s','U_\infty = 0.05 m/s','U_\infty = 0.08 m/s','U_\infty = 0.1 m/s','U_\infty = 0.2 m/s'];
set(figure,'units','pixel','position',[400 80 700 650])
% set(figure,'units','pixel','position',[400 80 300 250])
set(gca,'fontsize',12,'fontname','latex') 
for i=1:length(U)
     subplot(3,2,i)
     hold on
% Re_x=(x.*U(i))./visc;
Re_x=(x.*U(i))./visc(kk);
delta=5*x.*(Re_x).^(-0.5);
delta_t=del_t(kk).*x.*(Re_x).^(-0.5);
plot(x(1:3:end),delta(1:3:end),'-b','LineWidth',03)
plot(x(1:3:end),delta_t(1:3:end),'-r','LineWidth',03)
legend('\delta', '\delta_T')
title(char(titre(i)))
 box on
 grid on
 grid minor
 xlabel('x')
 ylabel('\delta (x)')
 end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Teta]=Teta_trapz(F2,bas,N,Eta,Pr)
Teta(1)=0;
for i=1:bas:N 
Teta(i+1)=trapz(F2(1:i+1).^Pr,Eta(1:i+1))./(trapz(F2.^Pr,Eta));
end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [f,g,h]=Euler(N,dn,h_1)
 h(1)=h_1;
 f(1)=0;
 g(1)=0;
for i=2:N
f(i)=f(i-1)+g(i-1).*dn;
g(i)=g(i-1)+h(i-1).*dn;
h(i)=h(i-1)-(f(i-1).*h(i-1).*dn)./2;
end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
