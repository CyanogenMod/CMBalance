<%inherit file="base.mako" />

<%def name="device_link(device)">
    % if request_type is None:
        /?device=${device}
    % else:
        /?device=${device}&type=${request_type}
    % endif
</%def>

<%def name="filter_link(type)">
    % if request_device is None:
        /?type=${type}
    % else:
        /?type=${type}&device=${request_device}
    % endif
</%def>

<%def name="filter_label()">
    % if request_device and request_type:
        - ${request_device|h} / ${request_type|h}
    % elif request_device and not request_type:
        - ${request_device|h}
    % elif request_type and not request_device:
        - ${request_type|h}
    % endif
</%def>

<h3>Browse Files ${filter_label()}</h3>
<div id="subnav">
<strong>Show Only:</strong> [ <a href="${filter_link('stable')}">stable</a> | <a href="${filter_link('nightly')}">nightly</a> ]
</div>

<table>
    <tr>
        <th>Device</th>
        <th>Type</th>
        <th>Filename</th>
        <th>Size</th>
        <th>Date Added</th>
    </tr>
    % for file in files:
    <% device=file.device.name %>
    <tr>
        <td><a href="${device_link(device)}">${file.device.name|h}</a></td>
        <td>${file.type}</td>
        <td>
            <img src="/static/rommanager.png" alt="Send to ROMManager"/>
            <a href="/get/${file.filename}">${file.filename|h}</a>
            <br/>
            <small class="md5">md5sum: ${file.md5sum|h}</small>
        </td>
        <td><small>${file.human_size|h}</small></td>
        <td><small>${file.date_created|h}</small></td>
    </tr>
    % endfor
</table>