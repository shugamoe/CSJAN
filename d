Help on module datetime:

NNAAMMEE
    datetime - Fast implementation of the datetime type.

MMOODDUULLEE  RREEFFEERREENNCCEE
    http://docs.python.org/3.4/library/datetime
    
    The following documentation is automatically generated from the Python
    source files.  It may be incomplete, incorrect or include features that
    are considered implementation detail and may vary between Python
    implementations.  When in doubt, consult the module reference at the
    location listed above.

CCLLAASSSSEESS
    builtins.object
        date
            datetime
        time
        timedelta
        tzinfo
            timezone
    
    class ddaattee(builtins.object)
     |  date(year, month, day) --> date object
     |  
     |  Methods defined here:
     |  
     |  ____aadddd____(self, value, /)
     |      Return self+value.
     |  
     |  ____eeqq____(self, value, /)
     |      Return self==value.
     |  
     |  ____ffoorrmmaatt____(...)
     |      Formats self with strftime.
     |  
     |  ____ggee____(...)
     |      __ge__=($self, value, /)
     |      --
     |      
     |      Return self>=value.
     |  
     |  ____ggeettaattttrriibbuuttee____(self, name, /)
     |      Return getattr(self, name).
     |  
     |  ____ggtt____(self, value, /)
     |      Return self>value.
     |  
     |  ____hhaasshh____(self, /)
     |      Return hash(self).
     |  
     |  ____llee____(self, value, /)
     |      Return self<=value.
     |  
     |  ____lltt____(self, value, /)
     |      Return self<value.
     |  
     |  ____nnee____(self, value, /)
     |      Return self!=value.
     |  
     |  ____nneeww____(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ____rraadddd____(self, value, /)
     |      Return value+self.
     |  
     |  ____rreedduuccee____(...)
     |      __reduce__() -> (cls, state)
     |  
     |  ____rreepprr____(self, /)
     |      Return repr(self).
     |  
     |  ____rrssuubb____(self, value, /)
     |      Return value-self.
     |  
     |  ____ssttrr____(self, /)
     |      Return str(self).
     |  
     |  ____ssuubb____(self, value, /)
     |      Return self-value.
     |  
     |  ccttiimmee(...)
     |      Return ctime() style string.
     |  
     |  ffrroommoorrddiinnaall(...) from builtins.type
     |      int -> date corresponding to a proleptic Gregorian ordinal.
     |  
     |  ffrroommttiimmeessttaammpp(...) from builtins.type
     |      timestamp -> local date from a POSIX timestamp (like time.time()).
     |  
     |  iissooccaalleennddaarr(...)
     |      Return a 3-tuple containing ISO year, week number, and weekday.
     |  
     |  iissooffoorrmmaatt(...)
     |      Return string in ISO 8601 format, YYYY-MM-DD.
     |  
     |  iissoowweeeekkddaayy(...)
     |      Return the day of the week represented by the date.
     |      Monday == 1 ... Sunday == 7
     |  
     |  rreeppllaaccee(...)
     |      Return date with new specified fields.
     |  
     |  ssttrrffttiimmee(...)
     |      format -> strftime() style string.
     |  
     |  ttiimmeettuuppllee(...)
     |      Return time tuple, compatible with time.localtime().
     |  
     |  ttooddaayy(...) from builtins.type
     |      Current date or datetime:  same as self.__class__.fromtimestamp(time.time()).
     |  
     |  ttoooorrddiinnaall(...)
     |      Return proleptic Gregorian ordinal.  January 1 of year 1 is day 1.
     |  
     |  wweeeekkddaayy(...)
     |      Return the day of the week represented by the date.
     |      Monday == 0 ... Sunday == 6
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  ddaayy
     |  
     |  mmoonntthh
     |  
     |  yyeeaarr
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  mmaaxx = datetime.date(9999, 12, 31)
     |  
     |  mmiinn = datetime.date(1, 1, 1)
     |  
     |  rreessoolluuttiioonn = datetime.timedelta(1)
    
    class ddaatteettiimmee(date)
     |  datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])
     |  
     |  The year, month and day arguments are required. tzinfo may be None, or an
     |  instance of a tzinfo subclass. The remaining arguments may be ints.
     |  
     |  Method resolution order:
     |      datetime
     |      date
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  ____aadddd____(self, value, /)
     |      Return self+value.
     |  
     |  ____eeqq____(self, value, /)
     |      Return self==value.
     |  
     |  ____ggee____(...)
     |      __ge__=($self, value, /)
     |      --
     |      
     |      Return self>=value.
     |  
     |  ____ggeettaattttrriibbuuttee____(self, name, /)
     |      Return getattr(self, name).
     |  
     |  ____ggtt____(self, value, /)
     |      Return self>value.
     |  
     |  ____hhaasshh____(self, /)
     |      Return hash(self).
     |  
     |  ____llee____(self, value, /)
     |      Return self<=value.
     |  
     |  ____lltt____(self, value, /)
     |      Return self<value.
     |  
     |  ____nnee____(self, value, /)
     |      Return self!=value.
     |  
     |  ____nneeww____(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ____rraadddd____(self, value, /)
     |      Return value+self.
     |  
     |  ____rreedduuccee____(...)
     |      __reduce__() -> (cls, state)
     |  
     |  ____rreepprr____(self, /)
     |      Return repr(self).
     |  
     |  ____rrssuubb____(self, value, /)
     |      Return value-self.
     |  
     |  ____ssttrr____(self, /)
     |      Return str(self).
     |  
     |  ____ssuubb____(self, value, /)
     |      Return self-value.
     |  
     |  aassttiimmeezzoonnee(...)
     |      tz -> convert to local time in new timezone tz
     |  
     |  ccoommbbiinnee(...) from builtins.type
     |      date, time -> datetime with same date and time fields
     |  
     |  ccttiimmee(...)
     |      Return ctime() style string.
     |  
     |  ddaattee(...)
     |      Return date object with same year, month and day.
     |  
     |  ddsstt(...)
     |      Return self.tzinfo.dst(self).
     |  
     |  ffrroommttiimmeessttaammpp(...) from builtins.type
     |      timestamp[, tz] -> tz's local time from POSIX timestamp.
     |  
     |  iissooffoorrmmaatt(...)
     |      [sep] -> string in ISO 8601 format, YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM].
     |      
     |      sep is used to separate the year from the time, and defaults to 'T'.
     |  
     |  nnooww(tz=None) from builtins.type
     |      Returns new datetime object representing current time local to tz.
     |      
     |        tz
     |          Timezone object.
     |      
     |      If no tz is specified, uses local timezone.
     |  
     |  rreeppllaaccee(...)
     |      Return datetime with new specified fields.
     |  
     |  ssttrrppttiimmee(...) from builtins.type
     |      string, format -> new datetime parsed from a string (like time.strptime()).
     |  
     |  ttiimmee(...)
     |      Return time object with same time but with tzinfo=None.
     |  
     |  ttiimmeessttaammpp(...)
     |      Return POSIX timestamp as float.
     |  
     |  ttiimmeettuuppllee(...)
     |      Return time tuple, compatible with time.localtime().
     |  
     |  ttiimmeettzz(...)
     |      Return time object with same time and tzinfo.
     |  
     |  ttzznnaammee(...)
     |      Return self.tzinfo.tzname(self).
     |  
     |  uuttccffrroommttiimmeessttaammpp(...) from builtins.type
     |      timestamp -> UTC datetime from a POSIX timestamp (like time.time()).
     |  
     |  uuttccnnooww(...) from builtins.type
     |      Return a new datetime representing UTC day and time.
     |  
     |  uuttccooffffsseett(...)
     |      Return self.tzinfo.utcoffset(self).
     |  
     |  uuttccttiimmeettuuppllee(...)
     |      Return UTC time tuple, compatible with time.localtime().
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  hhoouurr
     |  
     |  mmiiccrroosseeccoonndd
     |  
     |  mmiinnuuttee
     |  
     |  sseeccoonndd
     |  
     |  ttzziinnffoo
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  mmaaxx = datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)
     |  
     |  mmiinn = datetime.datetime(1, 1, 1, 0, 0)
     |  
     |  rreessoolluuttiioonn = datetime.timedelta(0, 0, 1)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from date:
     |  
     |  ____ffoorrmmaatt____(...)
     |      Formats self with strftime.
     |  
     |  ffrroommoorrddiinnaall(...) from builtins.type
     |      int -> date corresponding to a proleptic Gregorian ordinal.
     |  
     |  iissooccaalleennddaarr(...)
     |      Return a 3-tuple containing ISO year, week number, and weekday.
     |  
     |  iissoowweeeekkddaayy(...)
     |      Return the day of the week represented by the date.
     |      Monday == 1 ... Sunday == 7
     |  
     |  ssttrrffttiimmee(...)
     |      format -> strftime() style string.
     |  
     |  ttooddaayy(...) from builtins.type
     |      Current date or datetime:  same as self.__class__.fromtimestamp(time.time()).
     |  
     |  ttoooorrddiinnaall(...)
     |      Return proleptic Gregorian ordinal.  January 1 of year 1 is day 1.
     |  
     |  wweeeekkddaayy(...)
     |      Return the day of the week represented by the date.
     |      Monday == 0 ... Sunday == 6
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from date:
     |  
     |  ddaayy
     |  
     |  mmoonntthh
     |  
     |  yyeeaarr
    
    class ttiimmee(builtins.object)
     |  time([hour[, minute[, second[, microsecond[, tzinfo]]]]]) --> a time object
     |  
     |  All arguments are optional. tzinfo may be None, or an instance of
     |  a tzinfo subclass. The remaining arguments may be ints.
     |  
     |  Methods defined here:
     |  
     |  ____bbooooll____(self, /)
     |      self != 0
     |  
     |  ____eeqq____(self, value, /)
     |      Return self==value.
     |  
     |  ____ffoorrmmaatt____(...)
     |      Formats self with strftime.
     |  
     |  ____ggee____(...)
     |      __ge__=($self, value, /)
     |      --
     |      
     |      Return self>=value.
     |  
     |  ____ggeettaattttrriibbuuttee____(self, name, /)
     |      Return getattr(self, name).
     |  
     |  ____ggtt____(self, value, /)
     |      Return self>value.
     |  
     |  ____hhaasshh____(self, /)
     |      Return hash(self).
     |  
     |  ____llee____(self, value, /)
     |      Return self<=value.
     |  
     |  ____lltt____(self, value, /)
     |      Return self<value.
     |  
     |  ____nnee____(self, value, /)
     |      Return self!=value.
     |  
     |  ____nneeww____(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ____rreedduuccee____(...)
     |      __reduce__() -> (cls, state)
     |  
     |  ____rreepprr____(self, /)
     |      Return repr(self).
     |  
     |  ____ssttrr____(self, /)
     |      Return str(self).
     |  
     |  ddsstt(...)
     |      Return self.tzinfo.dst(self).
     |  
     |  iissooffoorrmmaatt(...)
     |      Return string in ISO 8601 format, HH:MM:SS[.mmmmmm][+HH:MM].
     |  
     |  rreeppllaaccee(...)
     |      Return time with new specified fields.
     |  
     |  ssttrrffttiimmee(...)
     |      format -> strftime() style string.
     |  
     |  ttzznnaammee(...)
     |      Return self.tzinfo.tzname(self).
     |  
     |  uuttccooffffsseett(...)
     |      Return self.tzinfo.utcoffset(self).
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  hhoouurr
     |  
     |  mmiiccrroosseeccoonndd
     |  
     |  mmiinnuuttee
     |  
     |  sseeccoonndd
     |  
     |  ttzziinnffoo
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  mmaaxx = datetime.time(23, 59, 59, 999999)
     |  
     |  mmiinn = datetime.time(0, 0)
     |  
     |  rreessoolluuttiioonn = datetime.timedelta(0, 0, 1)
    
    class ttiimmeeddeellttaa(builtins.object)
     |  Difference between two datetime values.
     |  
     |  Methods defined here:
     |  
     |  ____aabbss____(self, /)
     |      abs(self)
     |  
     |  ____aadddd____(self, value, /)
     |      Return self+value.
     |  
     |  ____bbooooll____(self, /)
     |      self != 0
     |  
     |  ____ddiivvmmoodd____(self, value, /)
     |      Return divmod(self, value).
     |  
     |  ____eeqq____(self, value, /)
     |      Return self==value.
     |  
     |  ____fflloooorrddiivv____(self, value, /)
     |      Return self//value.
     |  
     |  ____ggee____(...)
     |      __ge__=($self, value, /)
     |      --
     |      
     |      Return self>=value.
     |  
     |  ____ggeettaattttrriibbuuttee____(self, name, /)
     |      Return getattr(self, name).
     |  
     |  ____ggtt____(self, value, /)
     |      Return self>value.
     |  
     |  ____hhaasshh____(self, /)
     |      Return hash(self).
     |  
     |  ____llee____(self, value, /)
     |      Return self<=value.
     |  
     |  ____lltt____(self, value, /)
     |      Return self<value.
     |  
     |  ____mmoodd____(self, value, /)
     |      Return self%value.
     |  
     |  ____mmuull____(self, value, /)
     |      Return self*value.
     |  
     |  ____nnee____(self, value, /)
     |      Return self!=value.
     |  
     |  ____nneegg____(self, /)
     |      -self
     |  
     |  ____nneeww____(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ____ppooss____(self, /)
     |      +self
     |  
     |  ____rraadddd____(self, value, /)
     |      Return value+self.
     |  
     |  ____rrddiivvmmoodd____(self, value, /)
     |      Return divmod(value, self).
     |  
     |  ____rreedduuccee____(...)
     |      __reduce__() -> (cls, state)
     |  
     |  ____rreepprr____(self, /)
     |      Return repr(self).
     |  
     |  ____rrfflloooorrddiivv____(self, value, /)
     |      Return value//self.
     |  
     |  ____rrmmoodd____(self, value, /)
     |      Return value%self.
     |  
     |  ____rrmmuull____(self, value, /)
     |      Return value*self.
     |  
     |  ____rrssuubb____(self, value, /)
     |      Return value-self.
     |  
     |  ____rrttrruueeddiivv____(self, value, /)
     |      Return value/self.
     |  
     |  ____ssttrr____(self, /)
     |      Return str(self).
     |  
     |  ____ssuubb____(self, value, /)
     |      Return self-value.
     |  
     |  ____ttrruueeddiivv____(self, value, /)
     |      Return self/value.
     |  
     |  ttoottaall__sseeccoonnddss(...)
     |      Total seconds in the duration.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  ddaayyss
     |      Number of days.
     |  
     |  mmiiccrroosseeccoonnddss
     |      Number of microseconds (>= 0 and less than 1 second).
     |  
     |  sseeccoonnddss
     |      Number of seconds (>= 0 and less than 1 day).
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  mmaaxx = datetime.timedelta(999999999, 86399, 999999)
     |  
     |  mmiinn = datetime.timedelta(-999999999)
     |  
     |  rreessoolluuttiioonn = datetime.timedelta(0, 0, 1)
    
    class ttiimmeezzoonnee(tzinfo)
     |  Fixed offset from UTC implementation of tzinfo.
     |  
     |  Method resolution order:
     |      timezone
     |      tzinfo
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  ____eeqq____(self, value, /)
     |      Return self==value.
     |  
     |  ____ggee____(...)
     |      __ge__=($self, value, /)
     |      --
     |      
     |      Return self>=value.
     |  
     |  ____ggeettiinniittaarrggss____(...)
     |      pickle support
     |  
     |  ____ggtt____(self, value, /)
     |      Return self>value.
     |  
     |  ____hhaasshh____(self, /)
     |      Return hash(self).
     |  
     |  ____llee____(self, value, /)
     |      Return self<=value.
     |  
     |  ____lltt____(self, value, /)
     |      Return self<value.
     |  
     |  ____nnee____(self, value, /)
     |      Return self!=value.
     |  
     |  ____nneeww____(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ____rreepprr____(self, /)
     |      Return repr(self).
     |  
     |  ____ssttrr____(self, /)
     |      Return str(self).
     |  
     |  ddsstt(...)
     |      Return None.
     |  
     |  ffrroommuuttcc(...)
     |      datetime in UTC -> datetime in local time.
     |  
     |  ttzznnaammee(...)
     |      If name is specified when timezone is created, returns the name.  Otherwise returns offset as 'UTC(+|-)HH:MM'.
     |  
     |  uuttccooffffsseett(...)
     |      Return fixed offset.
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  mmaaxx = datetime.timezone(datetime.timedelta(0, 86340))
     |  
     |  mmiinn = datetime.timezone(datetime.timedelta(-1, 60))
     |  
     |  uuttcc = datetime.timezone.utc
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from tzinfo:
     |  
     |  ____ggeettaattttrriibbuuttee____(self, name, /)
     |      Return getattr(self, name).
     |  
     |  ____rreedduuccee____(...)
     |      -> (cls, state)
    
    class ttzziinnffoo(builtins.object)
     |  Abstract base class for time zone info objects.
     |  
     |  Methods defined here:
     |  
     |  ____ggeettaattttrriibbuuttee____(self, name, /)
     |      Return getattr(self, name).
     |  
     |  ____nneeww____(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ____rreedduuccee____(...)
     |      -> (cls, state)
     |  
     |  ddsstt(...)
     |      datetime -> DST offset in minutes east of UTC.
     |  
     |  ffrroommuuttcc(...)
     |      datetime in UTC -> datetime in local time.
     |  
     |  ttzznnaammee(...)
     |      datetime -> string name of time zone.
     |  
     |  uuttccooffffsseett(...)
     |      datetime -> timedelta showing offset from UTC, negative values indicating West of UTC

DDAATTAA
    MMAAXXYYEEAARR = 9999
    MMIINNYYEEAARR = 1
    ddaatteettiimmee__CCAAPPII = <capsule object "datetime.datetime_CAPI">

FFIILLEE
    /usr/lib/python3.4/datetime.py

