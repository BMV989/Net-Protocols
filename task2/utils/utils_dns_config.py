from typeclasses.creator_typeclasses.record_a import RecordTypeA
from typeclasses.creator_typeclasses.record_aaaa import RecordTypeAAAA
from typeclasses.creator_typeclasses.record_answer import Answer
from typeclasses.creator_typeclasses.record_cname import RecordTypeCNAME
from typeclasses.creator_typeclasses.record_mx import RecordTypeMX
from typeclasses.creator_typeclasses.record_ns import RecordTypeNS
from typeclasses.creator_typeclasses.record_ptr import RecordTypePTR
from typeclasses.creator_typeclasses.record_soa import RecordTypeSoa


def creators_from_answers(array: list, holder: list):
    for answer in array:
        rdata = ''

        match answer.type_record:
            case 'A':
                rdata = RecordTypeA(answer.rdata.ip)
            case 'AAAA':
                rdata = RecordTypeAAAA(answer.rdata.ip)
            case 'CNAME':
                rdata = RecordTypeCNAME(answer.rdata.cname)
            case 'MX':
                rdata = RecordTypeMX(answer.rdata.preference, answer.rdata.mail_exchange)
            case 'NS':
                rdata = RecordTypeNS(answer.rdata.name_server)
            case 'PTR':
                rdata = RecordTypePTR(answer.rdata.name_server)
            case 'SOA':
                rdata = RecordTypeSoa(answer.rdata.primary_server, answer.rdata.responsible_authority,
                                      answer.rdata.serial_number, answer.rdata.refresh_interval,
                                      answer.rdata.retry_interval, answer.rdata.expire_limit, answer.rdata.minimum_ttl)

        ans = Answer(answer.name, answer.type_record, answer.class_record, answer.ttl, rdata)
        holder.append(ans)


def to_creator(answer):
    rdata = ''

    match answer.type_record:
        case 'A':
            rdata = RecordTypeA(answer.rdata.ip)
        case 'AAAA':
            rdata = RecordTypeAAAA(answer.rdata.ip)
        case 'CNAME':
            rdata = RecordTypeCNAME(answer.rdata.cname)
        case 'MX':
            rdata = RecordTypeMX(answer.rdata.preference, answer.rdata.mail_exchange)
        case 'NS':
            rdata = RecordTypeNS(answer.rdata.name_server)
        case 'PTR':
            rdata = RecordTypePTR(answer.rdata.name_server)
        case 'SOA':
            rdata = RecordTypeSoa(answer.rdata.primary_server, answer.rdata.responsible_authority,
                                  answer.rdata.serial_number, answer.rdata.refresh_interval,
                                  answer.rdata.retry_interval, answer.rdata.expire_limit, answer.rdata.minimum_ttl)
    return rdata
