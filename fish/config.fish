# GLOBAL VARIALBLES
set -gx EDITOR nvim
set -gx THEME dark

# set fish colors to match rose-pine theme
set fish_color_autosuggestion 56526e
set fish_color_command 9ccfd8
set fish_color_param f6c177


if status is-interactive
  # Commands to run in interactive sessions can go here
end

function fish_greeting
  neofetch --config $HOME/.config/neofetch/configs/sm3.conf
end

function clr
  set_color $argv
end
function clrbg
  set_color --background $argv
end

function prompt__jobs
  for job in (jobs)
    printf '%s  %s\n' (clr 908caa) $job
  end
end

function prompt__status
  if [ $cmd__status -ne 0 ]
    clrbg eb6f92 191724
    echo -n '  '
    clrbg c4a7e7 eb6f92
    echo -n ''
  end
  clr normal
end

function prompt__date
  set -l hours (date +%I)
  set -l minutes (date +%M)
  set -l ampm (date +%P)
  set -l day (date +%a)
  set -l month (date +%b)
  set -l date (date +%d)

  clrbg c4a7e7 191724
  echo -n " $day, $month $date"
  clrbg f6c177 c4a7e7
  echo -n ''
  clrbg f6c177 191724
  echo -n " $hours:$minutes $ampm"
  clrbg 9ccfd8 f6c177
  echo -n ''
  clr normal
end

function prompt__battery
  set -l lvl (cat /sys/class/power_supply/BAT0/capacity)
  set -l sts (cat /sys/class/power_supply/BAT0/status)
  set -l icon
  set -l chargingicon
  set -l batteryclr '9ccfd8' '191724'

  if test $sts = 'Charging'
    set chargingicon ''
  end

  if [ $lvl -ge 96 -a $lvl -le 100 ]
    set icon ''
  end
  if [ $lvl -ge 90 -a $lvl -le 95 ]
    set icon ''
  end
  if [ $lvl -ge 80 -a $lvl -le 89 ]
    set icon ''
  end
  if [ $lvl -ge 70 -a $lvl -le 79 ]
    set icon ''
  end
  if [ $lvl -ge 60 -a $lvl -le 69 ]
    set icon ''
  end
  if [ $lvl -ge 50 -a $lvl -le 59 ]
    set icon ''
  end
  if [ $lvl -ge 40 -a $lvl -le 49 ]
    set icon ''
  end
  if [ $lvl -ge 30 -a $lvl -le 39 ]
    set icon ''
  end
  if [ $lvl -ge 20 -a $lvl -le 29 ]
    set icon ''
  end
  if [ $lvl -ge 10 -a $lvl -le 19 ]
    set icon ''
  end
  if [ $lvl -ge 1 -a $lvl -le 9 ]
    set icon ''
  end

  if [ $sts != 'Charging' -a $lvl -le 20 ]
    set lowbattery '!!!'
    clrbg 9ccfd8 --bold d7827e
  else
    clrbg 9ccfd8 191724
  end

  echo -n " $icon $lvl% $chargingicon$lowbattery"
  clrbg black 9ccfd8; echo -n ''; clr normal
end

function prompt__user
  if fish_is_root_user
    printf '%s%s ' (clr --bold f6c177) (string upper $USER)
  else
    printf '%s%s ' (clr --bold e0def4) (string upper $USER)
  end
  clr normal
end

function prompt__git
  if test fish_git_prompt
    clr 908caa
    echo -n ''(fish_git_prompt) ''
  end
  clr normal
end

function fish_prompt
  set -g cmd__status $status
  prompt__jobs
  prompt__status
  prompt__date
  prompt__battery
  echo
  prompt__user
  prompt__git
  set_color normal
end

function fish_right_prompt
  clrbg black ebbcba
  echo -n ''
  clrbg ebbcba 191724
  echo -n (prompt_pwd)
  echo -n ' '
  clr normal
end
