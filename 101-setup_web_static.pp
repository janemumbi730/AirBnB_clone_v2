# Install Nginx
package { 'nginx':
  ensure => 'installed',
}

# Create necessary directories if they don't exist
file { '/data/web_static/releases/test/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
  recurse => true,
}

file { '/data/web_static/shared/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
  recurse => true,
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => '<html>
    <head>
    </head>
    <body>
      Holberton School
    </body>
  </html>',
}

# Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test/',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Update Nginx configuration
file_line { 'nginx_hbnb_static':
  path    => '/etc/nginx/sites-available/default',
  line    => "        location /hbnb_static/ {\n            alias /data/web_static/current/;\n        }",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Ensure Nginx is running and enabled
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Package['nginx'],
}

