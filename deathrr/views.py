import json

from django.shortcuts import render
import datetime
from django.utils import timezone
from .models import DeceasedEntry, DeceasedCodes, ICDCode
from .forms import DeceasedEntryForm, NewCodeForm
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required
from django.db import connections
import pandas as pd
from django.shortcuts import HttpResponse


@login_required(login_url="/users/login")
def home_view(request):
    states = [ "-----",
        "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO",
        "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO",
        "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA",
        "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA",
        "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE",
        "NEW JERSEY", "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA",
        "OHIO", "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA",
        "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA",
        "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING"
    ]

    special_filters = ["-----", "All Reports", "All Reports in Date Range", "All Reports with No Codes", "All Reports with 'Pending Investigation'"]

    if request.GET.get('filter_start_date'):
        start_date = request.GET.get('filter_start_date')
        request.session['start_date'] = start_date
    elif request.GET.get('filter_end_date'):
        end_date = request.GET.get('filter_end_date')
        request.session['end_date'] = end_date
    if request.session.get('start_date'):
        start_date = datetime.datetime.strptime(request.session.get('start_date'), '%Y-%m-%d').date()
    else:
        start_date = datetime.date.today()
    if request.session.get('end_date'):
        end_date = datetime.datetime.strptime(request.session.get('end_date'), '%Y-%m-%d').date()
    else:
        end_date = datetime.date.today()
    filter_state = request.session.get('state', '-----')
    filter_text = request.session.get('filter_text', '')
    filter_code = request.session.get('filter_code', '')
    filter_primary = request.session.get('filter_primary', False)
    special_filter = request.session.get('special_filter', "-----")

    return render(request, 'deathrr/home.html', {'start_date': start_date, 'end_date': end_date, 'filter_code': filter_code, 'states':states, 'selected_state': filter_state, 'filter_text': filter_text,
                                                 'filter_primary': filter_primary, 'special_filters': special_filters, 'selected_special_filter': special_filter})


@login_required(login_url="/users/login")
def filter_reports_view(request):
    if request.GET.get('special_filter'):
        request.session['special_filter'] = request.GET.get('special_filter')
    elif request.GET.get('filter_start_date'):
        request.session['start_date'] = request.GET.get('filter_start_date')
    elif request.GET.get('filter_end_date'):
        request.session['end_date'] = request.GET.get('filter_end_date')
    elif request.GET.get('filter_primary'):
        request.session['filter_primary'] = True if request.GET.get('filter_primary') == "on" else False
    elif request.GET.get('filter_state'):
        request.session['state'] = request.GET.get('filter_state')
    elif request.GET.get('filter_text'):
        request.session['filter_text'] = request.GET.get('filter_text')
    elif 'filter_text' in request.GET and not request.GET.get('filter_text'):
        request.session['filter_text'] = ""
    else:
        request.session['filter_primary'] = False
    start_date = request.session.get('start_date', str(datetime.date.today()))
    end_date = request.session.get('end_date', str(datetime.date.today()))

    # added_start_time = datetime.timedelta(hours=0, minutes=0, seconds=0)
    # added_time = datetime.timedelta(hours=23, minutes=59, seconds=59)
    # start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    # start_date += added_start_time
    # start_date = timezone.make_aware(start_date)
    # end_date += added_time
    # end_date = timezone.make_aware(end_date)

    filter_primary = request.session.get('filter_primary', False)
    special_filter = request.session.get('special_filter', "-----")
    state = request.session.get('state', '-----')
    filter_text = request.session.get('filter_text', '')
    if special_filter == "-----":
        if state == '-----':
            filtered_reports = DeceasedEntry.objects.filter(dod__gte=start_date, dod__lte=end_date, deleted_flag=0).order_by('dod')
        else:
            filtered_reports = DeceasedEntry.objects.filter(dod__gte=start_date, dod__lte=end_date, state_where_died=state, deleted_flag=0).order_by('dod')
        if filter_text != '':
            if is_code(filter_text):
                report_ids = filtered_reports.values_list('id', flat=True)
                filter_code_id = ICDCode.objects.filter(code=filter_text).values_list('id', flat=True)

                if not filter_primary:
                    filtered_mapper = DeceasedCodes.objects.filter(deceased_id__in=report_ids, code_id__in=filter_code_id).values_list('deceased_id', flat=True)
                else:
                    filtered_mapper = DeceasedCodes.objects.filter(deceased_id__in=report_ids, code_id__in=filter_code_id, is_primary=1).values_list('deceased_id', flat=True)
                filtered_reports = filtered_reports.filter(id__in=filtered_mapper).order_by('dod')
                print(list(filtered_reports.values_list('id', flat=True)))
                request.session['download_count_data'] = json.dumps(list(filtered_reports.values_list('id', flat=True)))

                return render(request, 'deathrr/partials/report_list.html', {'reports': filtered_reports, 'reports_size': len(filtered_reports)})
            else:
                description_filtered_reports = []
                report_ids = filtered_reports.values_list('id', flat=True)
                codes_counter = {}
                filtered_codes = ICDCode.objects.filter(description__icontains=filter_text)
                if filter_primary:
                    filtered_mapper = DeceasedCodes.objects.filter(deceased_id__in=report_ids, is_primary=1).values_list('code_id', flat=True)
                else:
                    filtered_mapper = DeceasedCodes.objects.filter(deceased_id__in=report_ids).values_list('code_id', flat=True)
                code_dict = {code.id: code for code in filtered_codes}
                for code in filtered_mapper:
                    if code in code_dict:
                        if code in codes_counter:
                            codes_counter[code] += 1
                        else:
                            codes_counter[code] = 1
                if len(codes_counter) > 0:
                    for key in codes_counter.keys():
                        description_filtered_reports.append({'count': codes_counter[key], 'description': code_dict[key].description, 'code':code_dict[key].code})

                if len(description_filtered_reports) > 0:
                   description_filtered_reports = sorted(description_filtered_reports, key=lambda x: x['count'], reverse=True)
                request.session['download_count_data'] = json.dumps(description_filtered_reports)
                return render(request, 'deathrr/partials/report_list_count.html', {'reports': description_filtered_reports, 'reports_size': len(description_filtered_reports)})
        else:
            all_filtered_reports = []
            report_ids = filtered_reports.values_list('id', flat=True)
            codes_counter = {}
            if filter_primary:
                filtered_mapper = DeceasedCodes.objects.filter(deceased_id__in=report_ids, is_primary=1).values_list(
                    'code_id', flat=True)
            else:
                filtered_mapper = DeceasedCodes.objects.filter(deceased_id__in=report_ids).values_list('code_id', flat=True)
            for code in filtered_mapper:
                if code in codes_counter:
                    codes_counter[code] += 1
                else:
                    codes_counter[code] = 1
            if len(codes_counter) > 0:
                for key in codes_counter.keys():
                    curr_code = ICDCode.objects.get(id=key)
                    all_filtered_reports.append(
                        {'count': codes_counter[key], 'description': curr_code.description,
                         'code': curr_code.code})

            if len(all_filtered_reports) > 0:
                all_filtered_reports = sorted(all_filtered_reports, key=lambda x: x['count'], reverse=True)
            request.session['download_count_data'] = json.dumps(all_filtered_reports)
            return render(request, 'deathrr/partials/report_list_count.html',
                          {'reports': all_filtered_reports, 'reports_size': len(filtered_reports)})
    elif special_filter == "All Reports in Date Range":
        all_reports = DeceasedEntry.objects.filter(dod__gte=start_date, dod__lte=end_date, deleted_flag=0).order_by('dod')
        request.session['download_count_data'] = json.dumps(list(all_reports.values_list('id', flat=True)))
        return render(request, 'deathrr/partials/report_list.html', {'reports': all_reports, 'reports_size': len(all_reports)})
    elif special_filter == "All Reports":
        all_reports = DeceasedEntry.objects.filter(deleted_flag=0).order_by('dod')
        request.session['download_count_data'] = json.dumps(list(all_reports.values_list('id', flat=True)))
        return render(request, 'deathrr/partials/report_list.html', {'reports': all_reports, 'reports_size': len(all_reports)})
    elif special_filter == "All Reports with No Codes":
        all_reports = DeceasedEntry.objects.filter(deleted_flag=0).order_by('dod')
        report_ids = all_reports.values_list('id', flat=True)
        codes_mapper = DeceasedCodes.objects.all().values_list('deceased_id', flat=True).distinct()
        no_code_ids = list(set(report_ids) - set(codes_mapper))
        all_reports = all_reports.filter(id__in=no_code_ids)
        request.session['download_count_data'] = json.dumps(list(all_reports.values_list('id', flat=True)))
        return render(request, 'deathrr/partials/report_list.html', {'reports': all_reports, 'reports_size': len(all_reports)})
    else:
        all_reports = DeceasedEntry.objects.filter(dod__gte=start_date, dod__lte=end_date, manner_of_death="Pending Investigation" ,deleted_flag=0).order_by('dod')
        request.session['download_count_data'] = json.dumps(list(all_reports.values_list('id', flat=True)))
        return render(request, 'deathrr/partials/report_list.html', {'reports': all_reports, 'reports_size': len(all_reports)})



def is_code(text):
    obj = ICDCode.objects.filter(code=text)
    is_code = False if not obj.exists() else True
    return is_code



@login_required(login_url="/users/login")
def create_deceased_report(request):
    if request.method == 'POST':
        form = DeceasedEntryForm(data=request.POST)
        if form.is_valid():
            saved_report = form.save()
            return redirect(reverse('deathrr:update_deceased_report', kwargs={'pk': saved_report.id}))
    else:
        form = DeceasedEntryForm()
    return render(request, 'deathrr/create_deceased_report.html', {'form': form})


@login_required(login_url="/users/login")
def update_deceased_report(request, pk):
    report = DeceasedEntry.objects.get(id=pk)
    modified_by = request.user.username
    form = DeceasedEntryForm(instance=report)
    if request.method == 'POST':
        form = DeceasedEntryForm(request.POST, instance=report)
        if form.is_valid():
            i = form.save(commit=False)
            i.modified_by = modified_by
            form.save()
            return redirect('deathrr:home')
    else:
        form = DeceasedEntryForm(instance=report)

    return render(request, 'deathrr/update_deceased_report.html', {'form': form, 'pk': pk})


@login_required(login_url="/users/login")
def view_deceased_report(request, pk):
    report = DeceasedEntry.objects.get(id=pk)
    try:
        codes = DeceasedCodes.objects.filter(deceased_id=pk)
        code_info = []
        for c in codes:
            icd_code = ICDCode.objects.get(id=c.code_id.id)
            code_info.append({'code': icd_code.code, 'description': icd_code.description, 'type': icd_code.type, 'is_primary': c.is_primary})
    except DeceasedCodes.DoesNotExist:
        codes = None
        code_info = []
    if codes:
        return render(request, 'deathrr/view_deceased_report.html', {'report': report, 'codes': code_info, 'codes_size': len(code_info)})
    else:
        return render(request, 'deathrr/view_deceased_report.html', {'report': report, 'codes': None, 'codes_size': 0})


@login_required(login_url="/users/login")
def delete_report(request, pk):
    report = DeceasedEntry.objects.get(id=pk)
    start_date = request.session.get('start_date', datetime.datetime.today())
    end_date = request.session.get('end_date', datetime.datetime.today())
    if report:
        report.deleted_flag = True
        report.save()
    filtered_reports = DeceasedEntry.objects.filter(dod__gte=start_date, dod__lte=end_date, deleted_flag=False).order_by('dod')
    request.session['download_count_data'] = json.dumps(list(filtered_reports.values_list('id', flat=True)))
    return render(request, 'deathrr/partials/report_list.html', {'reports': filtered_reports, 'reports_size': len(filtered_reports)})


@login_required(login_url="/users/login")
def add_code(request, pk):
    if request.method == 'POST':
        new_code_form = NewCodeForm(data=request.POST)
        if new_code_form.is_valid():
            DeceasedCodes.objects.create(
                deceased_id=DeceasedEntry.objects.get(id=pk),
                code_id=new_code_form.cleaned_data['code_id'],
                is_primary=new_code_form.cleaned_data['is_primary']
            )
    else:
        new_code_form = NewCodeForm()
    try:
        existing_codes = DeceasedCodes.objects.filter(deceased_id=pk)
        code_info = []
        for code in existing_codes:
            code_details = ICDCode.objects.get(id=code.code_id.id)
            code_info.append({'code': code_details.code, 'description': code_details.description, 'type': code_details.type,
                              'is_primary': code.is_primary, 'id': code.id})
    except DeceasedCodes.DoesNotExist:
        existing_codes = None
    if existing_codes:
        return render(request, 'deathrr/partials/deceased_codes_list.html',
                      {'existing_codes': code_info, 'codes_size': len(existing_codes),
                       'new_code_form': new_code_form, 'pk': pk})
    else:
        return render(request, 'deathrr/partials/deceased_codes_list.html',
                      {'existing_codes': existing_codes, 'codes_size': 0,
                       'new_code_form': new_code_form, 'pk':pk})


@login_required(login_url="/users/login")
def delete_deceased_code(request, d_pk, c_pk):
    new_code_form = NewCodeForm()
    code_to_delete = DeceasedCodes.objects.get(id=c_pk)
    if code_to_delete:
        code_to_delete.delete()
    try:
        existing_codes = DeceasedCodes.objects.filter(deceased_id=d_pk)
        code_info = []
        for code in existing_codes:
            code_details = ICDCode.objects.get(id=code.code_id.id)
            code_info.append({'code': code_details.code, 'description': code_details.description, 'type': code_details.type,
                              'is_primary': code.is_primary, 'id': code.id})
    except DeceasedCodes.DoesNotExist:
        existing_codes = None
    if existing_codes:
        return render(request, 'deathrr/partials/deceased_codes_list.html',
                      {'existing_codes': code_info, 'codes_size': len(existing_codes),
                       'new_code_form': new_code_form, 'pk': d_pk})
    else:
        return render(request, 'deathrr/partials/deceased_codes_list.html',
                      {'existing_codes': existing_codes, 'codes_size': 0,
                       'new_code_form': new_code_form, 'pk': d_pk})


@login_required(login_url="/users/login")
def find_and_add_icd_code(icd_code):
    code_exists = False
    potential_entry = ICDCode.objects.filter(code=icd_code)
    if not potential_entry.exists():
        with connections['RPMS'].cursor() as cursor:
            query = f"SELECT * FROM IHS.BVS_MORTALITY_ICD10 WHERE CODE='{icd_code}'"
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                ICDCode.objects.create(code=row.code, description=row.description, type='C')
                code_exists = True
    else:
        code_exists = True
    return code_exists


@login_required(login_url="/users/login")
def download_count_reports(request):
    data = request.session.get('download_count_data', None)
    if data:
        list_data = json.loads(data)
        cols = ['Count', 'Description', 'Code']
        tbl = []
        for i in list_data:
            tbl.append([i['count'], i['description'], i['code']])
        df = pd.DataFrame(tbl, columns=cols)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocuments.spreadsheetml.sheet')
        now = datetime.datetime.now()
        filename = now.strftime('death_r&r_data_%m%d%y_%H%M%S')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.xlsx'
        df.to_excel(response, index=False, engine='openpyxl')
        return response
    return 5


@login_required(login_url="/users/login")
def download_detail_reports(request):
    data = request.session.get('download_count_data', None)
    if data:
        list_data = json.loads(data)
        cols = ['Name', 'Chart Number', 'DOB', 'State', 'Death Certificate Number', 'DOD', 'Place of Death', 'Race', 'Autopsy Performed', 'Manner of Death', 'Was Work Related', 'Place of Injury', 'Method of Verification', 'Codes']
        tbl = []
        reports = DeceasedEntry.objects.filter(id__in=list_data)
        for report in reports:
            autopsy_performed = "Yes" if report.autopsy_performed == 1 else "No"
            was_work_injury = "Yes" if report.death_by_work_injury == 1 else "No"
            place_of_injury = "N/A" if not report.place_of_injury else report.place_of_injury
            report_codes = list(ICDCode.objects.filter(id__in=list(DeceasedCodes.objects.filter(deceased_id=report.id).values_list('code_id', flat=True))).values_list('code', flat=True))
            tbl.append([report.name, report.chart_num, report.dob, report.state_where_died, report.death_cert_num, report.dod, report.place_of_death, report.race, autopsy_performed, report.manner_of_death, was_work_injury, place_of_injury, report.method_of_verification, report_codes])

        df = pd.DataFrame(tbl, columns=cols)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocuments.spreadsheetml.sheet')
        now = datetime.datetime.now()
        filename = now.strftime('death_r&r_data_%m%d%y_%H%M%S')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.xlsx'
        df.to_excel(response, index=False, engine='openpyxl')
        return response
    return 5