
xf = 50; xb = -xf;  y = 50; zu = 20; zd = 50;
path = [xf y zd; xb y zd; xb y zu; xf y zu; xf y zd] * 1e-3;
p = mstraj(path, [], [0, 3, 0.25, 0.5, 0.25]', path(1,:), 0.01, 0);

% axis equal
% plot_arrow([path; path(1,:)], '1.5', 2)
% hold on
% grid
% xyzlabel
% yaxis(0,0)
% light; lighting gouraud
% hold off

stance = 1:300; reset = 300:400;
plot3(p(stance,1), stance*0.01, p(stance,3), 'b')
hold on
plot3(p(reset,1), reset*0.01, p(reset,3), 'r')

set(gca, 'Zdir', 'reverse')
xyzlabel
ylabel('Time (s)')
grid
view(72, 18)
zaxis(0.02, 0.05)


rvcprint('subfig', 'a', 'thicken', 2.5)

x = p(:,1);
clf
hold on
for i=1:4
    plot([1:400]*0.01, x( mod([1:400]+(i-1)*100, 400)+1) )
end
grid
xlabel('Time (s)')
ylabel('Foot x-coordinate (m)')
legend('Foot 1', 'Foot 2', 'Foot 3', 'Foot 4')

rvcprint('subfig', 'b', 'thicken', 1.5)
