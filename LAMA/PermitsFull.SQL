select p.numstring as [Permit Number]
	, pgd.[type] as [Type of Work]
	, p.d_filed as [Date Filed]
	, isnull(pgd.issuedate, '') as [Issue Date]
	, pgd.pin as [PIN]
	, pgd.[owner] as [Property Owner]
	, p.[address] as [Property Address]
	, pgd.contractors as [Contractors]
	, isnull(substring((
		select ',' + cgd.email
		from contact c
		inner join prmtk pk on pk.contactid = c.contactid
			and pk.prmtid = p.prmtid
			and pk.isdeleted = 0
		inner join contactgriddata cgd on cgd.contactid = pk.contactid
			and cgd.isdeleted = 0
		where c.isdeleted = 0
		For XML PATH ('')
	), 2, 1000), '') as [Contractor Contact Details]
	, pgd.constrval as [Cost of Construction]
	, isnull(firstfloor.value, 0) as [First Floor Area]
	, isnull(secondfloor.value, 0) as [Second Floor Area]
	, isnull(thirdfloor.value, 0) as [Third Floor Area]
	, pgd.landuse as [Land Use]
	, p.descr as [Description]
from prmt p
inner join prmtgriddata pgd on pgd.prmtid = p.prmtid
left join (
	select pf.prmtid
		, isnull(val, 0) as [value]
	from prmtfeat pf
	inner join prmtfeatprop pfp on pfp.prmtfeatid = pf.prmtfeatid
		and pfp.lu_prmtfeatpropid = 768
		and pfp.isdeleted = 0
	where pf.lu_prmtfeatid = 65
		and pf.isdeleted = 0		
) as firstfloor on firstfloor.prmtid = p.prmtid
left join (
	select pf.prmtid
		, isnull(val, 0) as [value]
	from prmtfeat pf
	inner join prmtfeatprop pfp on pfp.prmtfeatid = pf.prmtfeatid
		and pfp.lu_prmtfeatpropid = 770
		and pfp.isdeleted = 0
	where pf.lu_prmtfeatid = 65
		and pf.isdeleted = 0		
) as secondfloor on secondfloor.prmtid = p.prmtid
left join (
	select pf.prmtid
		, isnull(val, 0) as [value]
	from prmtfeat pf
	inner join prmtfeatprop pfp on pfp.prmtfeatid = pf.prmtfeatid
		and pfp.lu_prmtfeatpropid = 772
		and pfp.isdeleted = 0
	where pf.lu_prmtfeatid = 65
		and pf.isdeleted = 0		
) as thirdfloor on thirdfloor.prmtid = p.prmtid
where p.isdeleted = 0
	and p.submittaltype in(0, 1, 3)
order by p.d_filed desc
