import datetime
import os

import sublime
import sublime_plugin


def format_header(header, vars):
  for k, v in vars.items():
    if v:
      header = header.replace('<{}>'.format(k), v)
  return header


def get_header_for_file(file_name, project_settings, project_path):
  project_settings = project_settings.get('file_heading', {})
  header_file = project_settings.get('header_file', None)
  if header_file:
    header_file = os.path.join(project_path, header_file)
    vars = {
      'file_name': file_name,
      'year': str(datetime.datetime.now().year),
    }
    vars.update(project_settings.get('variables'))
    with open(header_file) as f:
      header = ''.join(f.readlines())
    return format_header(header, vars)


class InsertFileHeadingCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    project_data = window.project_data()
    project_path = window.extract_variables()['project_path']
    if project_data:
      header = get_header_for_file(self.view.file_name(), project_data.get('settings', {}), project_path)
      if header:
        self.view.insert(edit, 0, header)


class FileHeading(sublime_plugin.EventListener):
  def on_new(self, view):
    view.run_command('insert_file_heading')
