function log -a arg val -d 'Log to the console. -b=bold, -e=error, -i=info, -s=success, -w=warn'
  if test (count $argv) -le 1
    echo -en "$arg"
  else
    switch $arg
      case -b bold
        set_color -o; echo -en "$val"; set_color normal
      case -e err error
        set_color -o FF4A4A; echo -en "$val"; set_color normal
      case -i info
        set_color -o 0096FF; echo -en "$val"; set_color normal
      case -s success
        set_color -o 68B984; echo -en "$val"; set_color normal
      case -w warn
        set_color -o FF9551; echo -en "$val"; set_color normal
    end
  end
end

complete -c log -s b -d bold
complete -c log -s e -d error
complete -c log -s i -d info
complete -c log -s s -d success
complete -c log -s w -d warn
